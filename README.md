# 大学プロジェクト用
***  
## システム概要図  
![sal_system_overview](https://user-images.githubusercontent.com/35915885/83359919-66123280-a3b8-11ea-81f5-98a858e20511.png)  
Nodejsを動かしているのはraspberrypiです。  
今後の予定として直近のデータはRaspberryPiへ、過去のデータはAWSへ保存する予定が立てられましたが、後輩に託してあります。

***
* コードに関して  
modules = カメラユニット、センサユニットのプログラム  
web_pages = viewer内のプログラム。nodejs+expressです。  

参考文献  
* カメラ  
python+opencvとwebカメラを使って動体検知する話
https://ensekitt.hatenablog.com/entry/2018/06/11/200000  
この他にも様々なサイトにお世話になりました。

同班班員向けの使用方法(※あらかじめnodejsやらpythonやら必要なものは入れておいてください。)  
1,このリポジトリをcloneします。  
2,module内のma_X.X.pyをカメラモジュールにscpで送ります。  
3,cronやらrc.localで自動起動の設定をしておきます。  
4,ma_X.X.py内のscpの部分のipやらホスト名やらを適したものに変えてあげます。  
5,viewer/router内のsqlを使うページのipやらホストネームやらの設定を適したものに変えてあげます。  
6,node_modulesを全て削除し、npmやらexpressやら全てのモジュールのインストール,設定を行う。  
7,reboot  


以上で起動します。また、映像を撮って勝手に送って必要なフォルダに入ってnodejsが勝手に拾って、sqlが勝手に動作して、センサも認識を始めます。  
ipアドレスの静的な設定の仕方を忘れた？そんなあなたにはドングルです。hostapdの例のやつです。マニュアルを見てください。  
(3月追記)できればドングルは使わないほうがいいです。熱を持ちやすいので運用の際に不具合が起きがちになります。
