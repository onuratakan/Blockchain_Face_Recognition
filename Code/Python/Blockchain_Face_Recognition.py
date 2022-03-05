from base64 import encode
import difflib
import cv2
import dlib
import face_recognition
import json
from web3 import Web3
import web3

ganache_url = "HTTP://127.0.0.1:7545" 
web3 = Web3(Web3.HTTPProvider(ganache_url)) #Ortamın url'si tanıtıldı

#Ganache Üzerinde işlem yapacak hesabın indexi tanıtıldı
web3.eth.defaultAccount = web3.eth.accounts[0]

#Kontrata ait abi değerleri (js kodları), agabey adlı değişkene aktarıldı
agabey = json.loads('[{"inputs": [],"name": "retrieve","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "string","name": "_yazi","type": "string"}],"name": "store","outputs": [],"stateMutability": "nonpayable","type": "function"}]')
adres = web3.toChecksumAddress("0x5dD36815CEeF217D813899047d28cEFdF1800491")#Derlenen Kontratın Adresi

#Derlenen kontratın abi değerleri ve adresi, Kontrat adlı değişkene atandı
Kontrat = web3.eth.contract(address = adres, abi = agabey)

if web3.isConnected():#Tanımlanan ağın ayakta olup olmadığı kontrol edildi
    #Duzgun.jpg dosyasını duzgun değişkenine atadı
    duzgun = face_recognition.load_image_file("C:\\DERS\\PROJELER\\Python\\Kimlik\\images\\Duzgun.jpg")
    duzgun_encod = face_recognition.face_encodings(duzgun)[0]

    #önceden eğitilmiş HOG + Linear SVM yüz dedektörünü, detector e atadık.
    detector = dlib.get_frontal_face_detector()

    #Varsayılan kameranın açılmaısı sağlandı
    capt = cv2.VideoCapture(0)

    while True:

        ret,frame = capt.read()

        #yüz kordinatlarını atamak için değişken oluşturuldu
        locations =[]
        #yakalanan götüntüleri dedektörden geçirerek yüzler e atar
        faces = detector (frame)

        for face in faces: #yakalanan yüzlerin
            x = face.left()
            y = face.top()
            w = face.right()
            h = face.bottom()
            locations.append((y,w,h,x)) #değerler lokasyona atandı

        #Bilgisayarın anlaması için, verileri matrislere dönüştürdük
        face_encoding = face_recognition.face_encodings(frame, locations)

        #Matris üzerinde gezinmek için for açıldı
        i=0
        k=False #kişinin sisteme girdiğini belirlemek için değişken oluşturuldu

        for face in face_encoding:
            y,w,h,x = locations[i] #Lokasyondaki değerler değişkenlere tekrar atandı

            #compara_faces komutu ile iyi yüz arasında kerşılaştırma yapıldı ve bool değer dönderildi
            sonuc = face_recognition.compare_faces([duzgun_encod], face)

            if sonuc[0] == True: #Doğru ise
                #bir çerçeve oluşturuldu (frame, çerçevenin başlayacağı kodrinat, biteceği kordinat, rengi, kalınlığı)
                cv2.rectangle(frame, (x,y), (w,h), (0,255,0), 2)
                #Metin Eklendi (frame, text, stringin kordinatları, yazı tipi, yazi boyutu, rengi, kalınlığı)
                cv2.putText(frame, "Duzgun", (x,h+35), cv2.FONT_HERSHEY_PLAIN, 2,(0,0,255),2)
                k=True #Yüz tanıma sistemi, kullanıcıyı tanırsa k değeri True olur
            
            else:
                cv2.rectangle(frame, (x,y), (w,h), (0,255,0), 2)
                cv2.putText(frame, "Yabanci", (x,h+35), cv2.FONT_HERSHEY_PLAIN, 2,(0,0,255),2)

        cv2.imshow("Yuz Tanima",frame)#Pencere açılır

        if cv2.waitKey(10) & 0xFF == ord("q"):#Sistemden çıkmak için ullanılır
            break

    capt.release()
    cv2.destroyAllWindows()

if k == True:
    islem_hash = Kontrat.functions.store("Duzgun adli kullanici, yuz tanıma sistemi ile giris yapmistir").transact()

    print("Islemin hash degeri: ", islem_hash)
    #zincirden değer okunduğu için print kullanıldı