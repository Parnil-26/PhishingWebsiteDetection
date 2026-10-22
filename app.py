import ipaddress
import math
import re
from pathlib import Path
from urllib.parse import urlparse

import joblib
import pandas as pd
import streamlit as st


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="PhishGuard | Phishing URL Detector",
    page_icon="🛡️",
    layout="centered",
)

MODEL_PATH = Path(__file__).resolve().parent / "phishguard_model.pkl"

FEATURE_COLUMNS = [
    "url_length",
    "has_ip_address",
    "dot_count",
    "https_flag",
    "url_entropy",
    "token_count",
    "subdomain_count",
    "query_param_count",
    "tld_length",
    "path_length",
    "has_hyphen_in_domain",
    "number_of_digits",
    "tld_popularity",
    "suspicious_file_extension",
    "domain_name_length",
    "percentage_numeric_chars",
]


@st.cache_resource
def load_model():
    """Load the Random Forest model saved with joblib to a .pkl file."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH.name}. "
            "Place phishguard_model.pkl in the same folder as app.py."
        )
    return joblib.load(MODEL_PATH)


def extract_features(url: str) -> pd.DataFrame:
    """Extract the same 16 URL features used when training the model."""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path
    query = parsed.query
    domain_without_port = domain.split(":")[0]

    url_length = len(url)
    has_ip_address = int(
        re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", domain_without_port) is not None
    )
    dot_count = url.count(".")
    https_flag = int(parsed.scheme == "https")

    if url:
        frequencies = {}
        for char in url:
            frequencies[char] = frequencies.get(char, 0) + 1
        url_entropy = 0.0
        for count in frequencies.values():
            probability = count / len(url)
            url_entropy -= probability * math.log2(probability)
    else:
        url_entropy = 0.0

    tokens = [token for token in re.split(r"[/\-_.?=&:]+", url) if token]
    token_count = len(tokens)

    domain_parts = domain_without_port.split(".")
    subdomain_count = max(len(domain_parts) - 2, 0)
    query_param_count = 0 if not query else len(query.split("&"))
    tld = domain_parts[-1] if len(domain_parts) > 1 else ""
    tld_length = len(tld)
    path_length = len(path)
    has_hyphen_in_domain = int("-" in domain_without_port)
    number_of_digits = sum(char.isdigit() for char in url)

    common_tlds = {"com", "org", "net", "edu", "gov", "in", "co", "uk", "de", "io"}
    tld_popularity = int(tld.lower() in common_tlds)

    suspicious_extensions = (".exe", ".scr", ".zip", ".rar", ".bat", ".cmd", ".msi", ".apk")
    suspicious_file_extension = int(any(path.lower().endswith(ext) for ext in suspicious_extensions))
    domain_name_length = len(domain_without_port)
    percentage_numeric_chars = number_of_digits / len(url) * 100 if url else 0.0

    values = [
        url_length,
        has_ip_address,
        dot_count,
        https_flag,
        url_entropy,
        token_count,
        subdomain_count,
        query_param_count,
        tld_length,
        path_length,
        has_hyphen_in_domain,
        number_of_digits,
        tld_popularity,
        suspicious_file_extension,
        domain_name_length,
        percentage_numeric_chars,
    ]
    return pd.DataFrame([values], columns=FEATURE_COLUMNS)


st.title("🛡️ PhishGuard")
st.write("Machine Learning Based Phishing URL Detection")
st.info("Enter a URL such as https://example.com. The result is an ML prediction, not a guarantee of safety.")

url_input = st.text_input("Enter a URL to check:", placeholder="https://example.com")

if st.button("🔍 Check URL", use_container_width=True):
    if not url_input.strip():
        st.warning("Please enter a URL.")
    else:
        cleaned_url = url_input.strip()
        normalized_url = cleaned_url if cleaned_url.startswith(("http://", "https://")) else "http://" + cleaned_url
        parsed = urlparse(normalized_url)

        if parsed.scheme not in ("http", "https") or not parsed.hostname or "." not in parsed.hostname:
            st.error("Please enter a valid URL with a domain, such as https://example.com")
        else:
            try:
                model = load_model()
                features_df = extract_features(cleaned_url)
                st.subheader("Extracted URL features")
                st.dataframe(features_df.T.rename(columns={0: "Value"}), use_container_width=True)

                prediction = int(model.predict(features_df)[0])
                st.subheader("Prediction Result")

                if prediction == 0:
                    st.error("⚠️ Potential Phishing URL")
                elif prediction == 1:
                    st.success("✅ Classified as Legitimate")
                else:
                    st.warning(f"The model returned an unexpected class: {prediction}")

                if hasattr(model, "predict_proba"):
                    probabilities = model.predict_proba(features_df)[0]
                    class_probabilities = dict(zip(model.classes_, probabilities))
                    phishing_probability = float(class_probabilities.get(0, 0.0))
                    legitimate_probability = float(class_probabilities.get(1, 0.0))
                    col1, col2 = st.columns(2)
                    col1.metric("Phishing probability", f"{phishing_probability * 100:.2f}%")
                    col2.metric("Legitimate probability", f"{legitimate_probability * 100:.2f}%")

                st.caption("Predictions are based on URL features and are not a security guarantee.")
            except Exception as exc:
                st.error(f"Prediction failed: {exc}")

st.divider()
st.caption("PhishGuard academic project • Random Forest classifier")
