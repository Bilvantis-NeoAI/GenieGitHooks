#!/usr/bin/env python3
"""
Test script to verify encryption/decryption functionality
Run this to ensure the encryption is working properly before building the executable
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def encrypt_data(request_data):
    """Encrypt data using AES encryption with static key and IV."""
    try:
        # Static key and IV (must be bytes) - same as backend
        key = b'1234567890123456'  # 16 bytes key (AES-128)
        iv = b'abcdefghijklmnop'   # 16 bytes IV

        # Convert input string to bytes
        if isinstance(request_data, str):
            request_data = request_data.encode()

        # PKCS7 Padding for block size 16 bytes
        pad_len = 16 - len(request_data) % 16
        padded_data = request_data + bytes([pad_len] * pad_len)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        # Return base64 encoded string
        return base64.b64encode(encrypted).decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

def decrypt_data(encrypted_data):
    """Decrypt data using AES decryption with static key and IV."""
    try:
        # Static key and IV (must be bytes) - same as backend
        key = b'1234567890123456'  # 16 bytes key (AES-128)
        iv = b'abcdefghijklmnop'   # 16 bytes IV

        # Base64 decode the encrypted data
        encrypted_bytes = base64.b64decode(encrypted_data)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()

        # Remove PKCS7 padding
        pad_len = decrypted_padded[-1]
        decrypted = decrypted_padded[:-pad_len]

        # Return decrypted data as UTF-8 string
        return decrypted.decode('utf-8')

    except Exception as e:
        print(f"Decryption error: {e}")
        return None

def test_encryption_decryption():
    test_cases = [
        "Test@123",
        "mypassword",
        "ComplexPassword123!@#",
        "simple",
        "a",  # Single character
        "This is a longer password with spaces and symbols !@#$%^&*()"
    ]
    
    print("🔐 Testing Encryption/Decryption...")
    print("=" * 50)
    
    all_passed = True
    
    for i, original_text in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{original_text}'")
        
        # Encrypt the original text
        encrypted = encrypt_data(original_text)
        if not encrypted:
            print("❌ Encryption failed")
            all_passed = False
            continue
            
        print(f"✅ Encrypted: {encrypted}")
        
        # Decrypt the encrypted text
        decrypted = decrypt_data(encrypted)
        if not decrypted:
            print("❌ Decryption failed")
            all_passed = False
            continue
            
        print(f"✅ Decrypted: '{decrypted}'")
        
        # Verify result
        if decrypted == original_text:
            print("✅ Match: Original and decrypted text are identical")
        else:
            print(f"❌ Mismatch: Original='{original_text}', Decrypted='{decrypted}'")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Encryption/Decryption is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    test_encryption_decryption() 

#!/usr/bin/env python3
"""
Test script to verify encryption/decryption functionality
Run this to ensure the encryption is working properly before building the executable
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def encrypt_data(request_data):
    """Encrypt data using AES encryption with static key and IV."""
    try:
        # Static key and IV (must be bytes) - same as backend
        key = b'1234567890123456'  # 16 bytes key (AES-128)
        iv = b'abcdefghijklmnop'   # 16 bytes IV

        # Convert input string to bytes
        if isinstance(request_data, str):
            request_data = request_data.encode()

        # PKCS7 Padding for block size 16 bytes
        pad_len = 16 - len(request_data) % 16
        padded_data = request_data + bytes([pad_len] * pad_len)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        # Return base64 encoded string
        return base64.b64encode(encrypted).decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

def decrypt_data(encrypted_data):
    """Decrypt data using AES decryption with static key and IV."""
    try:
        # Static key and IV (must be bytes) - same as backend
        key = b'1234567890123456'  # 16 bytes key (AES-128)
        iv = b'abcdefghijklmnop'   # 16 bytes IV

        # Base64 decode the encrypted data
        encrypted_bytes = base64.b64decode(encrypted_data)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()

        # Remove PKCS7 padding
        pad_len = decrypted_padded[-1]
        decrypted = decrypted_padded[:-pad_len]

        # Return decrypted data as UTF-8 string
        return decrypted.decode('utf-8')

    except Exception as e:
        print(f"Decryption error: {e}")
        return None

def test_encryption_decryption():
    test_cases = [
        "Test@123",
        "mypassword",
        "ComplexPassword123!@#",
        "simple",
        "a",  # Single character
        "This is a longer password with spaces and symbols !@#$%^&*()"
    ]
    
    print("🔐 Testing Encryption/Decryption...")
    print("=" * 50)
    
    all_passed = True
    
    for i, original_text in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{original_text}'")
        
        # Encrypt the original text
        encrypted = encrypt_data(original_text)
        if not encrypted:
            print("❌ Encryption failed")
            all_passed = False
            continue
            
        print(f"✅ Encrypted: {encrypted}")
        
        # Decrypt the encrypted text
        decrypted = decrypt_data(encrypted)
        if not decrypted:
            print("❌ Decryption failed")
            all_passed = False
            continue
            
        print(f"✅ Decrypted: '{decrypted}'")
        
        # Verify result
        if decrypted == original_text:
            print("✅ Match: Original and decrypted text are identical")
        else:
            print(f"❌ Mismatch: Original='{original_text}', Decrypted='{decrypted}'")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Encryption/Decryption is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    test_encryption_decryption() 

#!/usr/bin/env python3
"""
Test script to verify encryption/decryption functionality
Run this to ensure the encryption is working properly before building the executable
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def encrypt_data(request_data):
    """Encrypt data using AES encryption with static key and IV."""
    try:
        # Static key and IV (must be bytes) - same as backend
        key = b'1234567890123456'  # 16 bytes key (AES-128)
        iv = b'abcdefghijklmnop'   # 16 bytes IV

        # Convert input string to bytes
        if isinstance(request_data, str):
            request_data = request_data.encode()

        # PKCS7 Padding for block size 16 bytes
        pad_len = 16 - len(request_data) % 16
        padded_data = request_data + bytes([pad_len] * pad_len)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        # Return base64 encoded string
        return base64.b64encode(encrypted).decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

def decrypt_data(encrypted_data):
    """Decrypt data using AES decryption with static key and IV."""
    try:
        # Static key and IV (must be bytes) - same as backend
        key = b'1234567890123456'  # 16 bytes key (AES-128)
        iv = b'abcdefghijklmnop'   # 16 bytes IV

        # Base64 decode the encrypted data
        encrypted_bytes = base64.b64decode(encrypted_data)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()

        # Remove PKCS7 padding
        pad_len = decrypted_padded[-1]
        decrypted = decrypted_padded[:-pad_len]

        # Return decrypted data as UTF-8 string
        return decrypted.decode('utf-8')

    except Exception as e:
        print(f"Decryption error: {e}")
        return None

def test_encryption_decryption():
    test_cases = [
        "Test@123",
        "mypassword",
        "ComplexPassword123!@#",
        "simple",
        "a",  # Single character
        "This is a longer password with spaces and symbols !@#$%^&*()"
    ]
    
    print("🔐 Testing Encryption/Decryption...")
    print("=" * 50)
    
    all_passed = True
    
    for i, original_text in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{original_text}'")
        
        # Encrypt the original text
        encrypted = encrypt_data(original_text)
        if not encrypted:
            print("❌ Encryption failed")
            all_passed = False
            continue
            
        print(f"✅ Encrypted: {encrypted}")
        
        # Decrypt the encrypted text
        decrypted = decrypt_data(encrypted)
        if not decrypted:
            print("❌ Decryption failed")
            all_passed = False
            continue
            
        print(f"✅ Decrypted: '{decrypted}'")
        
        # Verify result
        if decrypted == original_text:
            print("✅ Match: Original and decrypted text are identical")
        else:
            print(f"❌ Mismatch: Original='{original_text}', Decrypted='{decrypted}'")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Encryption/Decryption is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    test_encryption_decryption() 

#!/usr/bin/env python3
"""
Test script to verify encryption/decryption functionality
Run this to ensure the encryption is working properly before building the executable
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def encrypt_data(request_data):
    """Encrypt data using AES encryption with static key and IV."""
    try:
        # Static key and IV (must be bytes) - same as backend
        key = b'1234567890123456'  # 16 bytes key (AES-128)
        iv = b'abcdefghijklmnop'   # 16 bytes IV

        # Convert input string to bytes
        if isinstance(request_data, str):
            request_data = request_data.encode()

        # PKCS7 Padding for block size 16 bytes
        pad_len = 16 - len(request_data) % 16
        padded_data = request_data + bytes([pad_len] * pad_len)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        # Return base64 encoded string
        return base64.b64encode(encrypted).decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

def decrypt_data(encrypted_data):
    """Decrypt data using AES decryption with static key and IV."""
    try:
        # Static key and IV (must be bytes) - same as backend
        key = b'1234567890123456'  # 16 bytes key (AES-128)
        iv = b'abcdefghijklmnop'   # 16 bytes IV

        # Base64 decode the encrypted data
        encrypted_bytes = base64.b64decode(encrypted_data)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()

        # Remove PKCS7 padding
        pad_len = decrypted_padded[-1]
        decrypted = decrypted_padded[:-pad_len]

        # Return decrypted data as UTF-8 string
        return decrypted.decode('utf-8')

    except Exception as e:
        print(f"Decryption error: {e}")
        return None

def test_encryption_decryption():
    test_cases = [
        "Test@123",
        "mypassword",
        "ComplexPassword123!@#",
        "simple",
        "a",  # Single character
        "This is a longer password with spaces and symbols !@#$%^&*()"
    ]
    
    print("🔐 Testing Encryption/Decryption...")
    print("=" * 50)
    
    all_passed = True
    
    for i, original_text in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{original_text}'")
        
        # Encrypt the original text
        encrypted = encrypt_data(original_text)
        if not encrypted:
            print("❌ Encryption failed")
            all_passed = False
            continue
            
        print(f"✅ Encrypted: {encrypted}")
        
        # Decrypt the encrypted text
        decrypted = decrypt_data(encrypted)
        if not decrypted:
            print("❌ Decryption failed")
            all_passed = False
            continue
            
        print(f"✅ Decrypted: '{decrypted}'")
        
        # Verify result
        if decrypted == original_text:
            print("✅ Match: Original and decrypted text are identical")
        else:
            print(f"❌ Mismatch: Original='{original_text}', Decrypted='{decrypted}'")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Encryption/Decryption is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    test_encryption_decryption() 
    