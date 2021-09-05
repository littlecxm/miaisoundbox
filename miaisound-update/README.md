# miaisoundbox-update
prompt your miaisoundbox to update to the specified version.

Usage:<br/>
  1、fill the `user.ini` with your mi account and password<br/>
  2、run `xiaoai.py`,then if login success,you will need to choose the machine you want to update.<br/>
  3、if success, your miaisound-box will receive the update info and update by itself.<br/>

Notice:<br/>
  1、current just fully for X08A 、X08E to version 1.24.9<br/>
  2、for X08C just to version 1.24.8<br/>
  3、When you sign in with your mi account from a different location,you may fail.<br/>

NOTE:<br/>
  You can update X08C to version 1.24.9 by yourself.<br/>
  Maybe you need:
    {<br/>
    "name": "Redmi8",<br/>
    "hardware": "X08C",<br/>
    "link": "https://cdn.cnbj1.fds.api.mi-img.com/xiaoqiang/rom/x08c/payload_inc_1.24.8_1.24.9_de02b.bin",<br/>
    "hash": "828d744846e39a1f3e4a9175b51de02b",<br/>
    "extra": "{\\"FILE_HASH\\":\\"v1hikBCO5yhvjTJKserNxcThWV4dVYIqNrVokv9eojk=\\",\\"FILE_SIZE\\":\\"94517395\\",\\"METADATA_HASH\\":\\"a9aaHFy4voMIgUXz5e5DuE7KSn91QDuFRQmUU2NZaUQ=\\",\\"METADATA_SIZE\\":\"178915\\"}",<br/>
    "version": "1.24.9"<br/>
  }

Refer: https://github.com/azwhikaru/OpenMico <br/>
Refer: https://github.com/Yonsm/MiService<br/>
