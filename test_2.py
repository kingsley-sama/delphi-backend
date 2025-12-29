# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        start = head
        list_node = start.next
        i = 0
        current = None
        while i < n and list_node.next:
            list_node = list_node.next 
            i += 1
        current = list_node.next
        current = current.next
        list_node.next = current.next
        return start