## overall
토요일, 11 29 2025, 05:00 KST — 월요일, 12 01 2025, 07:00 KST
### Team Rank
* 6761 score
* #25
### diary
### forensic
`opb2` 파일이 맥북에어에 있어서 기억을 더듬어서 작성중... 파일을 까보면 php 프로젝트가 들어있을 것이다. /var/log/apache2 국룰 디렉토리에 들어가면 로그들이 있는데 이 로그를 확인해보면 python requests library인걸 숨기지도 않고 마구마구 호출하는 나쁜해커놈을 발견할 수 있다. 내가 문제를 푼 순서대로 얘기하자면 이 나쁜 해커놈이 삽질을 좀 하다가(사실삽질아님!) 마지막에 example.gif를 다운로드하는데 해당 경로에 가보면 gif는 어디로 가고 수상한 텍스트가 보인다. 
```
mbzTGN3mBbqOHr/h3/c2uebIG7VPft37SXR+hurPIglCYfLeFqIzSM/R9lLhKp5K;U+IiFdoC53E4vV+9aTeVHbsp/0YRYqDqQzvx0gBGpzIPAhEYlgd5SjpPPQOLgmmoCbWKLREBHparNdsK2BQ3tQ==;
```
base64인가 싶지만 디코딩은 안되고 중간에 ;로 끊어져있다. 이 example.gif는 뭘까 궁금해져서 해당경로 `/var/www/glpi/pics/screenshots/example.gif` 를 냅다 서치를 돌리면 auth.php에 백도어가 보인다. 해당 백도어를 기반으로 저 example.gif가 생성되었으므로 역으로 디코딩할수도 있다. 
```
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json

key = b"ec6c34408ae2523fe664bd1ccedc9c28"
iv = b"ecb2b0364290d1df"
ciphertext_b64 = "U+IiFdoC53E4vV+9aTeVHbsp/0YRYqDqQzvx0gBGpzIPAhEYlgd5SjpPPQOLgmmoCbWKLREBHparNdsK2BQ3tQ=="

cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_data = unpad(cipher.decrypt(base64.b64decode(ciphertext_b64)), AES.block_size)

result = json.loads(decrypted_data.decode('utf-8'))
print(result)
```
결과
```
{'login': 'albus.dumbledore', 'password': 'FawkesPhoenix#9!'}
```
타임라인을 정리해보자면 웹쉘 업로드로 Auth.php를 조작->example.gif생성->curl example.gif 뭐 이렇게 한것이다...

`opb3` 그럼 문제가 된 웹쉘은 무엇인가? setup.php를 보면 plugin.php의 submit_form이 `2b01d9d592da55cca64dd7804bc295e6e03b5df4` 인 경우에 웹쉘을 열어주는 백도어가 심어져 있다. 그리고 실제로 우리의 수상한 공격자 192.168.56.230씨는 해당 핸들러로 plugin.php에 요청을 많이많이 보내두었다. 그래서 나는 핸들러를 저 문자열이라고 생각했는데... 솔브를 못했으니 [공식롸업](https://github.com/HeroCTF/HeroCTF_v7/tree/master/Forensics/op-pensieve-breach-3)을 보자. 

내가 잘 이해한건진 모르겠지만 어쨌거나 plugin.php로 submit 한 것은 특정 데이터이고 이 데이터는 DB로 흘러들어간다. DB내부 데이터를 보기 위해서 DB를 직접 띄워보면 제출된 플러그인중에 어쩌구 정보가 있고 그걸 base64디코딩하면 어떤 author 정보가... 아니 문제에서는 분명 `Decoded identifier (without the flag wrapper) that the attacker encoded when registering the backdoor component`이게 author라는 뜻이라고? 아니 영어가 버겁다 맞는거같기도하고... 맞는듯.. 맞을지도... 나머지 정보는 이 DB를 뒤지면 나온다칸다... CVE찾는건 hijack the plugin loader라는 데에 주목했어야 하는 듯 하다. 

이벤트뷰어는 파이썬으로 4624기준으로 조지되 MS namespace를 잘 참조해서 짜면 되는듯 GUI 이벤트뷰어 정말 최악이고 나도 결국 파이썬으로 확인했는데 evtx에 익숙하지 않아서 그냥 접근한 ip정도만 확인할 수 있었다. 아니 내 코랩 데이터 날아감ㅡㅡ