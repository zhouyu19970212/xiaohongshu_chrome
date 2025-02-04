import ai_req
import tool
import Config
import log


ai_req.get_language_db()
a, b = ai_req.get_two_random_elements(Config.language_db['211_college'])
print(a)
print(b)
