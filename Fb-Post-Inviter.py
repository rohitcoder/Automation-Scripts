import requests 
import json
from bs4 import BeautifulSoup 
import urlparse 
burp0_url = "https://business.facebook.com/ufi/reaction/profile/browser/fetch/?limit=5000&total_count=5000&ft_ent_identifier=108566350975276&fb_dtsg_ag=AQxhzRLE9rpjfoRo1DHdRZ0DSQntKVunKgX-keo45t7N2Q:AQzSCWY38h7fU8ix7KUq66CzW1lEBK6d7q6b9qF1GVuNZA&__user=100005595064283&__a=1&__dyn=7AgSXghFoHG4Q9UrJDzk2mq2W8GA5FaDJ4WqK4UqwCGawIhEnUzgjGqK5-7oG5VGwJy9pUKbnyorxuF98SmquUuF3e16xqfzQdzoS6pvh4jUXVEO489EGicGdxO3i5VokKm8yElAx6u14xl0zCypHh43Hg-ezFEmUC1uCwDxe6UGq6UpxyWBGHzooAghwyzZ5CG2e4RVo8EiyXxK9z9ooK3m6ogUkBzUy4XCxS58hx2eyojz9eawzCJ1ymiQ2q6po_zoiKm2u10zUCcx22PxuE9kbzUgxCuV8y7EKUymEjyHGiawYyHDhoG26227Rh8C9xl28rgK7lAAAzE4y2O58gyUTyUbUmDwQwxG76u4UgwNx5e8xi8KUoyE-Uqze7Vojxy2q4UrxS0D8888US2m8wHy8C6EG4u11wk8Su6EaE8K&__csr=&__req=6p&__beoa=0&__pc=PHASED:media_manager_pkg&dpr=1&__ccg=GOOD&__rev=1002593526&__s=n5qgcm:rvmawv:n7hifk&__hsi=6866983610963240940-0&__comet_req=0&jazoest=27719&__jssesw=1&ft[tn]=-a"
burp0_cookies = {"datr": "ml9IXWc-hooQAZsZyGngW7lJ", "sb": "ml9IXey4Kv58ugWsRrgQRXp0", "_ga": "GA1.2.214750873.1587879017", "locale": "en_GB", "js_ver": "3892", "m_pixel_ratio": "1", "c_user": "100005595064283", "cppo": "1", "spin": "r.1002593322_b.trunk_t.1598811628_s.1_v.2_", "xs": "21%3AsAWFX-g9ae4V2A%3A2%3A1598775154%3A13272%3A4196%3A%3AAcVcdyV0_LJR0gJjSBqRwuoQhJhaDp_QlOYidiEqYKA", "fr": "1tpMIwMyIepQeqj6i.AWVuLZHlce-HqooJiS_WNa_2Daw.BdwSBm.qI.F9L.0.0.BfTGNk.AWVJSO_U", "presence": "EDvF3EtimeF1598844249EuserFA21B05595064283A2EstateFDt3F_5bDiFA2user_3a1B02305073382A2EoF1EfF1C_5dEutc3F1598844020217G598844020283CEchF_7bCC", "wd": "799x766"}
burp0_headers = {"Connection": "close", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36", "Viewport-Width": "799", "Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*", "Origin": "https://business.facebook.com", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://business.facebook.com/creatorstudio/?mode=facebook&content_table=ALL_POSTS&post_status=ALL&tab=content_posts&post_type=ALL&collection_id=free_form_collection", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9,hi;q=0.8,es;q=0.7,lt;q=0.6"}
list_response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
json_resp = json.loads(list_response.text[9:]) 
list_html = json_resp["domops"][0][3]["__html"] 
soup = BeautifulSoup(list_html, 'html.parser')
peoples_ids_list = soup.findAll("a", {"class":"_42ft _4jy0 _4jy3 _517h _51sy"})
invite_count = len(peoples_ids_list)
print("Inviting "+str(invite_count)+" peoples")
for people_id in peoples_ids_list: 
	explode = urlparse.parse_qs(urlparse.urlparse(people_id["ajaxify"]).query)
	invitee = explode["invitee"][0]
	hash_value = explode["hash"][0] 
	content_id = explode["content_id"][0]
	page_id = explode["page_id"][0]
	ext = explode["ext"][0]
	burp0_url = "https://www.facebook.com:443/pages/post_like_invite/send/"
	burp0_data = {"invitee": invitee, "page_id": page_id, "ref": "pages_post_reactor_dialogue", "content_id": content_id, "ext": ext, "hash": hash_value, "__user": "100005595064283", "__a": "1", "__dyn": "7AgSXghFoHG4Q9UrJDzk2mq2W8GA5FaDJ4WqK4UqwCGawIhEnUzgjGqK5-7oG5VGwJy9pUKbnyorxuF98SmquUuF3e16xqfzQdzoS7_h4jUXVEO489EGicGdxO3i5VokKm8yEqx6u14xl0zCypHh43Hg-ezFEmUC1uCwDxe6UGq6UpxyWBGHzooAghwyzZ5CG2e4RVo8EiyXxK9z9ooK3m6ogUkBzUy4XCxS58hx2eyojz9eawzCJ1ymiQ2q6po_zoiKm2u10zUCcx22PxuE9kbzUgxCuV8y7EKUymEjyHGiawYyHDhoG26227Rh8C9xl28rgK7lAAAzE4y2O58gyUTyUbUmDwQwxG76u4UgwNx5e8xi8KUoyE-Uqze7Vojxy2q4UrxS0D8888US2m8wHxa6EG4u11wk8Su6EaE8K", "__csr": '', "__req": "4q", "__beoa": "0", "__pc": "PHASED:media_manager_pkg", "dpr": "1", "__ccg": "GOOD", "__rev": "1002593526", "__s": "2m0lki:rvmawv:n7hifk", "__hsi": "6866983610963240940-0", "__comet_req": "0", "fb_dtsg": "AQFcQOBaGXMB:AQH33OAOqtrg", "jazoest": "21987", "__jssesw": "1"} 
	response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
	final_Response = json.loads(response.text[9:])
	if final_Response.has_key("error"):
		print("Lets refresh our paramter values")
		print(final_Response["errorDescription"])
		break;
	else:
		print("Invited successfully...")  
