
import streamlit as st
import pandas as pd
import joblib
import ipaddress
from urllib.parse import urlparse

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Phishing Website Detector",
    page_icon="🛡️",
    layout="centered"
)

# -----------------------------
# Load Trained Model
# -----------------------------
@st.cache_resource
def load_model():
    return joblib.load("phishing_model.joblib")

artifact = load_model()
model = artifact["model"]
FEATURE_NAMES = artifact["feature_names"]

# -----------------------------
# URL Feature Extraction
# Must match training code
# -----------------------------
SUSPICIOUS_WORDS = [
    "login", "verify", "update", "secure", "account",
    "banking", "signin", "password", "confirm", "wallet"
]

SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co",
    "is.gd", "cutt.ly", "rb.gy"
}

def extract_features(url):
    parsed = urlparse(
        url if "://" in url else "//" + url
    )

    hostname = (parsed.hostname or "").lower()

    # Check whether the hostname is an IP address
    try:
        ipaddress.ip_address(hostname)
        is_ip = 1
    except ValueError:
        is_ip = 0

    domain_parts = hostname.split(".") if hostname else []

    features = {
        "URLLength": len(url),
        "DomainLength": len(hostname),
        "NoOfDots": hostname.count("."),
        "NoOfHyphens": url.count("-"),
        "NoOfSubdomains": max(0, len(domain_parts) - 2),
        "IsDomainIP": is_ip,
        "HasAtSymbol": int("@" in url),
        "HasHTTPS": int(parsed.scheme.lower() == "https"),
        "NoOfDigits": sum(ch.isdigit() for ch in url),
        "NoOfQueryParams": len([
            item for item in parsed.query.split("&") if item
        ]),
        "HasSuspiciousKeyword": int(
            any(word in url.lower() for word in SUSPICIOUS_WORDS)
        ),
        "IsShortener": int(hostname in SHORTENER_DOMAINS)
    }

    # Preserve the exact feature order used during training
    return pd.DataFrame(
        [[features[name] for name in FEATURE_NAMES]],
        columns=FEATURE_NAMES
    )

# -----------------------------
# User Interface
# -----------------------------
st.title("🛡️ Phishing Website Detector")

st.write(
    "Check whether a URL appears suspicious using a "
    "Machine Learning model trained to identify phishing websites."
)

st.info(
    "Enter a complete URL, such as https://example.com"
)

url = st.text_input(
    "Enter Website URL",
    placeholder="https://example.com"
)

if st.button("🔍 Check Website", use_container_width=True):
    if not url.strip():
        st.warning("Please enter a URL first.")

    else:
        cleaned_url = url.strip()
        parsed_url = urlparse(
            cleaned_url if "://" in cleaned_url
            else "//" + cleaned_url
        )

        if (
            parsed_url.scheme.lower() not in ("http", "https")
            or not parsed_url.hostname
            or "." not in parsed_url.hostname
        ):
            st.error(
                "Please enter a valid URL with a domain, "
                "such as https://example.com"
            )

        else:
            try:
                input_features = extract_features(cleaned_url)
                prediction = int(model.predict(input_features)[0])

                st.subheader("Prediction Result")

                if prediction == 0:
                    st.error("⚠️ Potential Phishing Website")
                    st.write(
                        "The model classified this URL as phishing. "
                        "Avoid entering passwords or sensitive information."
                    )
                else:
                    st.success("✅ Classified as Legitimate")
                    st.write(
                        "The model classified this URL as legitimate. "
                        "This is not a guarantee that the website is safe."
                    )

            except Exception as e:
                st.error(f"Prediction failed: {e}")

st.divider()

st.caption(
    "Academic ML project • Decision Tree classifier • "
    "Predictions are based on URL features and are not a security guarantee."
)
