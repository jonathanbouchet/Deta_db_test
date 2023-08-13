import re

class Validator:
    def validate_username(self, username: str) -> bool:
        """
        Checks the validity of the entered username.
        Parameters
        ----------
        username: str
            The usernmame to be validated.

        Returns
        -------
        bool
            Validity of entered username.
        """
        pattern = r"^[a-zA-Z0-9_-]{1,20}$"
        return bool(re.match(pattern, username))

    def validate_name(self, name: str) -> bool:
        """
        Checks the validity of the entered name.
        Parameters
        ----------
        name: str
            The name to be validated.

        Returns
        -------
        bool
            Validity of entered name.
        """
        return 1 < len(name) < 100

    def validate_email(self, email: str) -> bool:
        """
        Checks the validity of the entered email.
        Parameters
        ----------
        email: str
            The email to be validated.
        Returns

        -------
        bool
            Validity of entered email.
        """
        pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return True if re.fullmatch(pattern, email) else False
        # return "@" in email and 2 < len(email) < 320
