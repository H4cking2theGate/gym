const CryptoJS = require('crypto-js');
function aes_encrypt(plainText, AES_KEY, AES_IV) {
  var encrypted = CryptoJS.AES.encrypt(plainText, CryptoJS.enc.Utf8.parse(AES_KEY), {
    iv: CryptoJS.enc.Utf8.parse(AES_IV)
  });
  return CryptoJS.enc.Base64.stringify(encrypted.ciphertext)
}