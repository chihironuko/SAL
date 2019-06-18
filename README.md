# 大学プロジェクト用
***
modules = カメラユニット、センサユニットのプログラム  
web_pages = viewer内のプログラム。nodejs+expressです。  
参考文献  
•カメラ  
python+opencvとwebカメラを使って動体検知する話
https://ensekitt.hatenablog.com/entry/2018/06/11/200000  
この他にも様々なサイトにお世話になりました。
  
  
正直ラズパイの中身が一番新しいなんてこともあるので、あまり当てにはしないでください。  

同班班員向けの使用方法(※あらかじめnodejsやらpythonやら必要なものは入れておいてください。)  
1,このリポジトリをcloneします。  
2,module内のma_X.X.pyをカメラモジュールにscpで送ります。  
3,cronやらrc.localで自動起動の設定をしておきます。  
4,ma_X.X.py内のscpの部分のipやらホスト名やらを適したものに変えてあげます。  
5,viewer/router内のsqlを使うページのipやらホストネームやらの設定を適したものに変えてあげます。  
6,node_modulesを全て削除し、npmやらexpressやら全てのモジュールのインストール,設定をおこなってください。面倒くさそうに見えて全く面倒ではありません。  
7,rebootします。  


以上で起動します。また、映像を撮って勝手に送って必要なフォルダに入ってnodejsが勝手に拾って、sqlが勝手に動作して、センサも認識を始めます。  
もし起動しなければ、センサなら初期登録の例のやつだと思われます。カメラとその他は知りません。おそらくcronが悪いんじゃないでしょうか(適当)  
正直その度にデバッグしてあげるのが無難です。しっかり見てあげてください。  
ipアドレスの静的な設定の仕方を忘れた？そんなあなたにはドングルです。hostapdの例のやつです。マニュアルを見てください。  
また、ドングルは簡単に色々設定してくれますが熱を持ってすぐに死ぬという特徴を持っています。頑張りましょう(?)。  
もしドングルが無理であれば、静的ipです。etc/hosts/interfacesを覗いてあげてください。wlan 0の部分をstaticにしてip addressとmaskを設定しましょう。  
(3月追記)できればドングルは使わないほうがいいです。熱で壊れます。  

マニュアル原本へのリンク
https://drive.google.com/open?id=1q03TFeA1tk8HdIHBVjSVxvsRePY7AIwj
