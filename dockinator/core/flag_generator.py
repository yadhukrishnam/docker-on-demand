import hmac
import hashlib

SECRET_KEY = "ymn8WLtsN.vupF2JZP^qX3uXN(ENU$o"


class GenerateFlag:
    def __init__(self, team_name, challenge_name):
        self.team_name = team_name
        self.challenge_name = challenge_name

    def generate_flag(self):
        normalized_team_name = self.team_name.strip()
        normalized_challenge_name = self.challenge_name.strip()
        
        # Combine team name and challenge name
        data = f"{normalized_team_name}:{normalized_challenge_name}"
        print(data)
        
        # Generate HMAC using the combined data
        hmac_obj = hmac.new(
            SECRET_KEY.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha1
        )
        flag_value = hmac_obj.hexdigest()
        
        # Construct the flag
        flag = f"hackception{{{normalized_team_name}_{normalized_challenge_name}_{flag_value}}}"
        return flag

    def extract_team_name(submitted_flag):
        prefix = "hackception{"
        suffix = "}"
        if not submitted_flag.startswith(prefix) or not submitted_flag.endswith(suffix):
            return None
        content = submitted_flag[len(prefix) : -len(suffix)]
        parts = content.split("_", 1)
        if len(parts) != 2:
            return None
        return parts[0]

    def validate_flag(self, submitted_flag, team_name):
        extracted_team_name = self.extract_team_name(submitted_flag)
        if extracted_team_name != team_name.strip():
            return False
        expected_flag = self.generate_flag(team_name)
        return submitted_flag.strip() == expected_flag
