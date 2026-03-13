from construct_block import Block, Blockchain
import time

def test_mining_basic():
    chain = Blockchain()
    block = Block(1, time.time(), "Test TX", chain.get_latest_block().hash)
    chain.mine_block(block)
    assert block.hash.startswith('00'), "挖矿难度未满足"
    assert len(chain.chain) == 2, "区块未正确添加"
    print("✓ 挖矿基础测试通过")

def test_tamper_detection():
    chain = Blockchain()
    # 添加2个区块后篡改第1个
    for i in range(2):
        b = Block(i+1, time.time(), f"TX-{i}", chain.get_latest_block().hash)
        chain.mine_block(b)
    
    chain.chain[1].data = "HACKED"
    assert not chain.is_chain_valid(), "未检测到篡改！"
    print("✓ 防篡改测试通过")

if __name__ == "__main__":
    print("关翔文+241275014")
    test_mining_basic()
    test_tamper_detection()