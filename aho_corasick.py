from collections import deque

class ACAutomaton:
    start = ord('ァ')
    end = ord('ヿ')
    size = end - start + 1  # カタカナの範囲をカバーするのに必要なサイズ
    
    class AutomatonNode:
        def __init__(self, words=[]):
            self.words = words.copy()
            self.next = [None] * (ACAutomaton.size)
            self.fail = None

        def add_word(self, word):
            self.words.append(word)
 
    def __init__(self):
        self.root = self.AutomatonNode()

    def add(self, kana, word):
        if not kana:  # 空のカナリストをチェック
            return
            
        node = self.root
        for c in kana:
            try:
                n = ord(c) - self.start
                if n < 0 or n >= len(node.next):
                    # 範囲外の文字はスキップ
                    continue
                    
                if node.next[n] is None:
                    node.next[n] = self.AutomatonNode(node.words)
                node = node.next[n]
            except (TypeError, IndexError):
                # 問題のある文字をスキップし続行
                continue
                
        node.add_word(word)

    def set_failure_path(self):
        queue = deque()
        self.root.fail = self.root
        queue.append(self.root)
        while queue:
            current_node = queue.popleft()
            for i in range(len(current_node.next)):
                child = current_node.next[i]
                if child is not None:
                    queue.append(child)
                    while current_node.fail.next[i] is None and current_node.fail is not self.root:
                        current_node = current_node.fail
                    if current_node.fail.next[i] is not None:
                        child.fail = current_node.next[i]
                    else:
                        child.fail = self.root


    def print_tree(self, node=None, n=0):
        if node is None:
            node = self.root
        for i in range(len(node.next)):
            if node.next[i] is not None:
                print("  ----" * n + chr(self.start + i) + " " + " ".join(node.next[i].words))
                self.print_tree(node.next[i], n + 1)


if __name__ == '__main__':
    A = ACAutomaton()
    A.add("トリ", "鳥")
    A.add("トクガワ", "徳川")
    A.add("アサ", "朝")
    A.add("アサ", "麻")
    A.add("トリイ", "鳥居")
    A.add("イカ", "いか")
    A.print_tree()
    A.set_failure_path()