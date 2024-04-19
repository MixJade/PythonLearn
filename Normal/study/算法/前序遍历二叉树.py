# coding=utf-8
# @Time    : 2024/3/13 9:36
# @Software: PyCharm
class Node:
    """二叉树节点对象
    """

    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None


def pre_order_traversal(node: Node) -> None:
    """前序遍历：
    先访问根节点，然后遍历左子树，再遍历右子树

    :param node: 二叉树节点对象
    """
    if node is None:
        return
    print(node.data)
    pre_order_traversal(node.left)  # 递归: 先访问左节点
    pre_order_traversal(node.right)  # 递归: 后访问右节点


# 创建二叉树
#     1
#    / \
#   2   3
#  / \
# 4   5
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)

# 前序遍历二叉树
pre_order_traversal(root)
