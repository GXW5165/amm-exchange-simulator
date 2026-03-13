from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes
import hashlib
import json

# ===== 任务1：对交易数据签名（补全）=====
def sign_transaction(tx_dict, private_key):
    # TODO 补全下方代码：
    # 提示：① 将交易字典转为字符串(应用JSON序列化) ② 计算SHA256哈希 ③ 用私钥签名
     tx_string = json.dumps(tx_dict, sort_keys=True)
     tx_hash = hashlib.sha256(tx_string.encode()).digest()
     signature = private_key.sign(tx_hash, ec.ECDSA(utils.Prehashed(hashes.SHA256())))
     return signature
    

# ===== 任务2：验证签名 + 篡改检测（补全）=====
def verify_signature(tx_dict, signature, public_key):
    # TODO：用公钥验证签名是否匹配原始交易
    # 提示: try..except..结构; verify函数
    tx_string = json.dumps(tx_dict, sort_keys=True)
    tx_hash = hashlib.sha256(tx_string.encode()).digest()

    try:
        public_key.verify(signature, tx_hash, ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        return True
    except:
        return False

if __name__ == "__main__":
    # ===== 金融场景 =====
    # 用户A向用户B转账100元，生成交易数据
    tx_data = {
        "from": "Alice_pubkey_0x123",
        "to": "Bob_pubkey_0x456", 
        "amount": 100,
        "timestamp": "2026-03-13T10:00:00"
    }

    # ===== 生成密钥对（已提供）=====
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()
    print("密钥对生成完成...")

    signature = sign_transaction(tx_data, private_key)
    print(f"交易签名完成: {signature[:32]}...")

    # 正常验证
    is_valid = verify_signature(tx_data, signature, public_key)
    print(f"签名验证: {is_valid}")

    # 篡改测试：攻击者修改金额
    tampered_tx = tx_data.copy()
    tampered_tx["amount"] = 1000000
    is_tamper_detected = not verify_signature(tampered_tx, signature, public_key)
    print(f"篡改检测: {'成功🔒' if is_tamper_detected else '失败⚠️'}")