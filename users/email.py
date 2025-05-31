from djoser import email as djoser_email


class CustomActivationEmail(djoser_email.ActivationEmail):
    template_name = "users/email/activation.html"

    def get_subject(self):
        return "Activate your EcommerceAPI account"


class CustomPasswordResetEmail(djoser_email.PasswordResetEmail):
    template_name = "users/email/password_reset.html"

    def get_subject(self):
        return "Reset your EcommerceAPI password"


class CustomPasswordResetConfirmEmail(djoser_email.PasswordChangedConfirmationEmail):
    template_name = "users/email/password_reset_confirm.html"

    def get_subject(self):
        return "Your EcommerceAPI password has been changed"
