class ListNode:

    def __init__(self, value, parent_list):
        self.value = value
        self.prev = None
        self.next = None
        self.parent_list = parent_list

    def remove(self):
        self.parent_list.size -= 1
        if self.parent_list.head == self:
            self.parent_list.head = self.prev
        if self.parent_list.tail == self:
            self.parent_list.tail = self.next

        if self.prev is not None:
            self.prev.next = self.next
        if self.next is not None:
            self.next.prev = self.prev

        self.prev = None
        self.next = None

class DoublyLinkedList:

    def __init__(self, init_value):
        new_order_node = ListNode(init_value, self)

        self.head = new_order_node
        self.tail = new_order_node
        self.size = 1

    def add(self, value):
        new_order_node = ListNode(value, self)

        if self.head is None:
            self.head = new_order_node
            self.tail = new_order_node
        else:
            self.tail.prev = new_order_node
            new_order_node.next = self.tail
            self.tail = new_order_node

        self.size += 1

        return new_order_node
