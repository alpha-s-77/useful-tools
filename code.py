import os
import glob
import fitz
import getpass
#宣言
pathname=os.path.dirname(os.path.abspath(__file__))
pathsys =pathname+"/*.pdf"
PL=[]
permissions = fitz.PDF_PERM_ACCESSIBILITY
encryption = fitz.PDF_ENCRYPT_AES_256
#すでに暗号化されているか
def pdf_is_encrypted(file):
    pdf = fitz.Document(file)
    return pdf.isEncrypted

#暗号化
def ango(List):
    print("パスワード設定 暗号化")
    print("ownerパス無記入の場合は, ownerパス=userパスとなります")
    up=getpass.getpass(prompt="Input your USER Pass:")
    urp=getpass.getpass(prompt="Confirm your USER Pass:")
    op=getpass.getpass(prompt="Input your OWNER Pass:")
    orp=getpass.getpass(prompt="Confirm your OWNER Pass:")
    if(up==urp and op==orp):
        if(op==""):
            op=up
        for file_name in List:
            if not pdf_is_encrypted(file_name):
                doc = fitz.open(file_name)
                doc.save("output/"+file_name, owner_pw=op, user_pw=up, encryption=encryption, permissions=permissions)
            else:
                print("実行時エラー: "+ file_name + " はすでに暗号化されています")
    else:
        print("認証エラー: 2つのパスワードが一致していません")
        print("")
        ango(List)
    print("")
    print("全ファイルの処理を完了しました")
#復号化(パスワードを消去-->管理者パス必要/パスワードを変更-->管理者パス必要)
def hukugo(List):
    print("復号化")
    pw=getpass.getpass(prompt="Input your OWNER Pass:")
    for file_name in List:
        if pdf_is_encrypted(file_name):
            pdf = fitz.open(file_name)
            if pdf.authenticate(pw):
                pdf.save("output/"+file_name)
                print("Info: "+file_name+" は正常に復号化されました")
            else:
                print('承認エラー: '+file_name+" [正しいパスワードを入力してください]")
        else:
            print("実行時エラー: "+file_name+" は暗号化されていません")
    print("")
    print("全ファイルの処理を完了しました")
#管理ターミナル
def kanri():
    print("")
    print("PDF管理センター")
    print("")
    print("1. 次から1つ選んでください")
    print("[1] このディレクトリに対し一括適用")
    print("[2] ディレクトリ内1つのファイルに対してのみ適用")
    s1=input("Input:")
    if(s1=="1"):
        print("")
        print("このディレクトリのpdfファイルを読み込み中...")
        PL = glob.glob("*.pdf")
        if(len(PL)==0):
            print("エラー: PDFファイルが見つかりませんでした")
            kanri()
        else:
            print("読み込み完了")
    elif(s1=="2"):
        print("")
        print("ファイル名を入力してください (.pdfを含まない)")
        s12=input("Input:")
        PL=glob.glob(s12+".pdf")
        if(len(PL)==0):
            print("エラー: PDFファイルが見つかりませんでした")
            kanri()
        else:
            print("読み込み完了")
    else:
        print("入力エラー: 再度やり直してください")
        kanri()
    print("")
    print("2. 操作内容を選んでください")
    print("[1] 暗号化")
    print("[2] 復号化 (パスワード解除処理)")
    s2=input("Input:")
    if(s2=="1"):
        print("")
        ango(PL)
    elif(s2=="2"):
        print("")
        hukugo(PL)
    else:
        prunt("入力エラー: 再度やり直してください")
        kanri()


if __name__=="__main__":
    kanri()
