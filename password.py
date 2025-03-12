import streamlit as st
import re
import random
import string

# List of common weak passwords to blacklist
COMMON_PASSWORDS = ["password", "123456", "qwerty", "admin", "letmein", "welcome", "password123"]

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Length Check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long (12+ recommended).")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?/~`]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    # Blacklist Check
    if password.lower() in COMMON_PASSWORDS:
        score = 0
        feedback.append("❌ Password is too common and easily guessable.")

    # Strength Rating
    if score >= 5:
        feedback.append("✅ Strong Password! Great job!")
    elif score >= 3:
        feedback.append("⚠️ Moderate Password - Consider adding more security features.")
    else:
        feedback.append("❌ Weak Password - Improve it using the suggestions above.")

    return score, feedback

# Function to generate a strong password
def generate_strong_password(length=12):
    """Generate a strong password with a mix of characters."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+{}[]:;<>,.?/~`"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Streamlit App
def main():
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")

    # Title and Description
    st.title("🔐 Password Strength Meter")
    st.write("Check the strength of your password and get suggestions to improve it.")

    # Password History (stored in session state)
    if "password_history" not in st.session_state:
        st.session_state.password_history = []

    # Input for password
    password = st.text_input("Enter your password:", type="password", key="password_input")

    # Toggle password visibility
    show_password = st.checkbox("Show Password")
    if show_password:
        st.write(f"👀 Your Password: `{password}`")

    # Check password strength
    if password:
        score, feedback = check_password_strength(password)

        # Display password strength progress bar
        st.subheader("📊 Password Strength")
        st.progress(score / 5)  # Normalize score to 0-1 for progress bar

        # Display feedback
        st.subheader("🔍 Analysis & Feedback")
        for message in feedback:
            st.write(message)

        # Add current password to history (max 3 entries)
        if len(st.session_state.password_history) >= 3:
            st.session_state.password_history.pop(0)
        st.session_state.password_history.append(password)

        # Display password history
        st.subheader("📜 Password History")
        for idx, old_password in enumerate(st.session_state.password_history, 1):
            st.write(f"{idx}. `{old_password}`")

        # Suggest a strong password if the current one is weak
        if score < 5:
            st.subheader("💡 Need a stronger password?")
            password_length = st.slider("Select password length", 8, 20, 12)
            if st.button("Generate a Strong Password"):
                suggested_password = generate_strong_password(password_length)
                st.write(f"🔒 Suggested Password: `{suggested_password}`")
                st.code(suggested_password)  # Display password in a code block for easy copying

# Run the app
if __name__ == "__main__":
    main()