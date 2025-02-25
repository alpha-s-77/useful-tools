> [!WARNING]
> このプログラムはすべて日本語話者によって活用されることを想定しています。<br>
> This programme is intended to be utilised entirely by Japanese speakers.<br>
> I am not responsible for any disadvantages caused by using this programme. Use at your own risk.

# 1. このツールについて
 このツールは, 個人で開発され, まさしく私が利用するためだけに作られています。<br>
そのため, 私の需要によっては今後も機能追加がありえます。また, 利用される方は Issues での要望も可能ですが, 全てに答えるとは限りません。<br>
> [!Caution]
> 本プログラムを用いて発生した不利益について, 私は責任を持ちません。各自の責任において利用してください。
 # 2. 機能説明
  このツールには, 以下の各項に書かれた機能が含まれます。<br>
 ## [1]. PDFファイルの暗号化・復号ツール
 (1) パスワードを指定します。(暗号化の際は, 確認のためパスワードを2回入力します)<br>
 (2) ファイルを指定します (PDF)。<br>
(3-A) 暗号化 のとき<br>
 - パスワードにより暗号化し, ```filename_encrypted.pdf``` のように新規ファイルを作成されます。<br>

(3-B) 復号 のとき<br>

 - パスワードにより復号し, ```filename_decrypted.pdf``` のように新規ファイルを作成されます。<br>
> [!Caution]
> 1. パスワードを忘れると, 復元できません。十分に注意してください。<br>
> 2. 使用する際, まず最初に, バックアップを取って, 自分の環境で使えるかを確かめてから使用することを強く推奨します。

> [!Note]
> もともとのファイル名が, ```hogehoge.pdf``` であるとき,<br>
> 暗号化をすると, ```hogehoge_encrypted.pdf```<br>
> 復号をすると, ```hogehoge_decrypted.pdf``` <br>
> のように新規ファイルが作られます。

 ## [2]. JPGファイル名変更ツール
(1) まず, JPGが含まれるフォルダについて指定します。<br>
(2) そのフォルダ内について 以下に規則に則って名前を変更されます。<br>
- ⅰ. 撮影日 順に並び替える (昇順, 新しいほうが後ろにきます)<br>
ただし, 撮影日が取得できない場合ファイル名はそのままとし, 処理から外される <br>
- ⅱ. 並び替えたときの あるファイルの順番 を $i  (ただし, i=0,1,2,...)$ とします。<br>
このとき, あるファイルは ```[i] MMDD-hhmmss.jpg``` に改名されます。<br>
この日付 (MMDD-hhmmss) は日本時間でのもの (JST, GMT+09) ですので注意してください。<br>
> [!note]
> ファイル名の例示: ```[3] 0515-220131.jpg```<br>
> このファイルは フォルダ内で $4$ 番目に撮影され, その撮影日は 05/15, 時刻は 22時01分31秒です。<br>
> ファイル番号は $0$ から始まり, 撮影日は 日本時間でのものであることに注意してください。<br>
> 撮影日に "年" は含まれませんから, 例えば年ごとに分けた フォルダを作るか, このプログラムを改変して用いてください。<br>

> [!Caution]
> 変更前の名前は保存されません。事前にバックアップ等作成しておくと, 万が一の際に便利です。
