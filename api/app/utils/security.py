import jwt, datetime, os, pytz
from flask import jsonify, request
from dotenv import load_dotenv

class Security:
    # Carga las variables de entorno desde el archivo .env
    load_dotenv()

    token_secret = os.getenv('TOKEN_SECRET')
    tz = pytz.timezone("America/Argentina/Buenos_Aires")

    @staticmethod
    def generate_token(user):
        # Crea el payload del token
        payload = {
            "user": user.username,
            "password": user.password,
            "exp": datetime.datetime.now(Security.tz) + datetime.timedelta(hours=24),
            "iat": datetime.datetime.now(Security.tz)
        }
        return jwt.encode(payload, Security.token_secret, algorithm="HS256")


    @staticmethod
    def verify_token(headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            # if (len(encoded_token) > 0):
            try:
                payload = jwt.decode(encoded_token, Security.token_secret, algorithms=["HS256"])
                # roles = list(payload['roles'])
                #
                # if 'Administrator' in roles:
                #     return True
                return True
            except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                return False

        return False
