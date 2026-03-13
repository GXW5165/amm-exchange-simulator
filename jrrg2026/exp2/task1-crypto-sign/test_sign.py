from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import hashlib

from crypto_sign import sign_transaction, verify_signature

def run_tests():
    print("开始运行数字签名测试...\n")
    passed = 0
    total = 3
    
    # ===== 测试1：正常签名验证 =====
    try:
        private_key = ec.generate_private_key(ec.SECP256K1())
        public_key = private_key.public_key()
        tx = {"from": "A", "to": "B", "amount": 100}
        
        sig = sign_transaction(tx, private_key)
        assert sig is not None and len(sig) > 0, "签名不能为空"
        
        is_valid = verify_signature(tx, sig, public_key)
        assert is_valid == True, "正常交易应验证通过"
        
        print("✓ 测试1 通过：正常签名验证")
        passed += 1
    except Exception as e:
        print(f"❌ 测试1 失败：{e}")
    
    # ===== 测试2：篡改检测 =====
    try:
        tampered_tx = tx.copy()
        tampered_tx["amount"] = 999999  # 攻击者篡改金额
        
        is_tamper_detected = not verify_signature(tampered_tx, sig, public_key)
        assert is_tamper_detected == True, "应检测到交易篡改"
        
        print("✓ 测试2 通过：篡改交易被正确拒绝")
        passed += 1
    except Exception as e:
        print(f"❌ 测试2 失败：{e}")
    
    # ===== 测试3：错误公钥验证失败 =====
    try:
        wrong_private = ec.generate_private_key(ec.SECP256K1())
        wrong_public = wrong_private.public_key()
        
        is_wrong_rejected = not verify_signature(tx, sig, wrong_public)
        assert is_wrong_rejected == True, "错误公钥应验证失败"
        
        print("✓ 测试3 通过：错误公钥无法验证签名")
        passed += 1
    except Exception as e:
        print(f"❌ 测试3 失败：{e}")
    
    # ===== 输出总结 =====
    print(f"\n测试结果：{passed}/{total} 通过")
    if passed == total:
        print("数字签名模块功能正确 ✅")
        return True
    else:
        print("提示：检查哈希计算、签名编码或验证逻辑")
        return False

if __name__ == "__main__":
    print("关翔文+241275014")
    run_tests()