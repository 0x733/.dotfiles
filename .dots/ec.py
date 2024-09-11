from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import rsa, os
def a(b,c):return''.join([chr(((ord(d)-65+c)%26)+65)if d.isupper()else chr(((ord(d)-97+c)%26)+97)if d.islower()else d for d in b])
def e(b,c):return''.join([chr(((ord(d)-65-c)%26)+65)if d.isupper()else chr(((ord(d)-97-c)%26)+97)if d.islower()else d for d in b])
def f(b,c):return''.join([chr((ord(d)+ord(c[i%len(c)]))%256)for i,d in enumerate(b)])
def g(b,c):return''.join([chr((ord(d)-ord(c[i%len(c)]))%256)for i,d in enumerate(b)])
def h(b,c):i=os.urandom(16);j=Cipher(algorithms.AES(c),modes.CFB(i),backend=default_backend()).encryptor();return i+j.update(b.encode())+j.finalize()
def k(b,c):i,j=b[:16],b[16:];l=Cipher(algorithms.AES(c),modes.CFB(i),backend=default_backend()).decryptor();return l.update(j)+l.finalize()
def m(b,c):return rsa.encrypt(b.encode(),c)
def n(b,c):return rsa.decrypt(b,c).decode()
def o(b,c):return Fernet(c).encrypt(b.encode())
def p(b,c):return Fernet(c).decrypt(b).decode()
def q(b,c):r=os.urandom(12);s=Cipher(algorithms.ChaCha20(c,r),mode=None,backend=default_backend()).encryptor();return r+s.update(b.encode())+s.finalize()
def t(b,c):r,s=b[:12],b[12:];u=Cipher(algorithms.ChaCha20(c,r),mode=None,backend=default_backend()).decryptor();return u.update(s)+u.finalize()
def v():w=int(input("Seçin:\n1. AES-256\n2. RSA 4096-bit\n3. Fernet\n4. ChaCha20\n5. Sezar\n6. Vigenère\nSeçim (1-6): "));return w
def main():w=v();x,y,z=None,None,None
if w==1:x=os.urandom(32);y=input("Metni girin: ");z=h(y,x);print(f"Şifrelenmiş (AES-256): {z}");print(f"Çözülen: {k(z,x).decode()}")
elif w==2:(A,B)=rsa.newkeys(4096);y=input("Metni girin: ");z=m(y,A);print(f"Şifrelenmiş (RSA-4096): {z}");print(f"Çözülen: {n(z,B)}")
elif w==3:x=Fernet.generate_key();y=input("Metni girin: ");z=o(y,x);print(f"Şifrelenmiş (Fernet): {z}");print(f"Çözülen: {p(z,x)}")
elif w==4:x=os.urandom(32);y=input("Metni girin: ");z=q(y,x);print(f"Şifrelenmiş (ChaCha20): {z}");print(f"Çözülen: {t(z,x).decode()}")
elif w==5:x=int(input("Kaydırma miktarı: "));y=input("Metni girin: ");z=a(y,x);print(f"Şifrelenmiş (Sezar): {z}");print(f"Çözülen: {e(z,x)}")
elif w==6:x=input("Anahtar kelime: ");y=input("Metni girin: ");z=f(y,x);print(f"Şifrelenmiş (Vigenère): {z}");print(f"Çözülen: {g(z,x)}")
else:print("Geçersiz seçim!")
if __name__=="__main__":main()