from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class AVLtreeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

    def get_root(self,item_id):
        try:
            root = self.get_queryset().filter(item_id=item_id,root=True).first()
        except (ObjectDoesNotExist ,AttributeError):
            root = None

        return root

    def get_node_by_id(self,node_id):
        try:
            node = self.get_queryset().filter(id=node_id).first()
        except (ObjectDoesNotExist, AttributeError):
            node = None

        return node


    def get_left_by_node_id(self, node_id):
        try:
            node = self.get_queryset().filter(id=node_id).first().left
        except (ObjectDoesNotExist,AttributeError):
            node = None

        return node

    def get_right_by_node_id(self, node_id):
        try:
            node = self.get_queryset().filter(id=node_id).first().right
        except (ObjectDoesNotExist, AttributeError):
            node = None

        return node

    def insert(self,key, item_id, element_data):
        root=self.get_root(item_id)
        new_item = self.insert_helper( root, key, item_id, element_data)
        return new_item

    def insert_helper(self, root, key, item_id, element_data):

        # Step 1 - Perform normal BST
       
        if root:
            root_left_id = self.get_left_by_node_id(root.id)
            root_right_id = self.get_right_by_node_id(root.id)
            root_left=self.get_node_by_id(root_left_id)
            root_right=self.get_node_by_id(root_right_id)
        if not root or (isinstance(root,int) and root  < 0):
            is_root=False
            if not self.get_root(item_id):
                is_root=True

            new_element = self.create(item_id=item_id
                               ,element_data=element_data,
                               val=key,
                               root =is_root,
                               item_field_id=item_id)
            return new_element



        elif key < root.val:
            new_item = self.insert_helper(root_left, key,item_id,element_data)
            root_left = self.get_node_by_id(new_item.id)
            root.left = new_item.id
            root_right_id = self.get_right_by_node_id(root.id)
            root_right = self.get_node_by_id(root_right_id)
        else:
            new_item = self.insert_helper(root_right, key,item_id,element_data)
            root_right = self.get_node_by_id(new_item.id)
            root.right = new_item.id
            root_left_id = self.get_left_by_node_id(root.id)
            root_left = self.get_node_by_id(root_left_id)






        # Step 2 - Update the height of the
        # ancestor node
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))
        root.save()


        balance = self.getBalance(root)

        if balance > 1 and key < root_left.val:
            return self.rightRotate(root)

        # Case 2 - Right Right
        if balance < -1 and key > root_right.val:
            return self.leftRotate(root)

        # Case 3 - Left Right
        if balance > 1 and key > root_left.val:
            root.left = self.leftRotate(root_left).id
            root.save()
            return self.rightRotate(root)

        # Case 4 - Right Left
        if balance < -1 and key < root_right.val:
            root.right = self.rightRotate(root_right).id
            root.save()
            return self.leftRotate(root)

        return root

    # Recursive function to delete a node with
    # given key from subtree with given root.
    # It returns root of the modified subtree.
    def delete(self, root, key):

        # Step 1 - Perform standard BST delete
        if not root or (isinstance(root,int) and root  < 0):
            return root

        elif key < root.val:
            root.left = self.delete(root.left, key)

        elif key > root.val:
            root.right = self.delete(root.right, key)

        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.getMinValueNode(root.right)
            root.val = temp.val
            root.right = self.delete(root.right,
                                     temp.val)

        # If the tree has only one node,
        # simply return it
        if root is None:
            return root

        # Step 2 - Update the height of the
        # ancestor node
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Step 3 - Get the balance factor
        balance = self.getBalance(root)

        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)

        # Case 2 - Right Right
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)

        # Case 3 - Left Right
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # Case 4 - Right Left
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, z):

        y = self.get_node_by_id(z.right)
        T2 = self.get_node_by_id(y.left)

        # Perform rotation
        if y:
            y.left = z.id

        if T2:
            T2val= T2.id
            z_right_new_height = self.get_height_by_id(T2val)
        else:
            T2val = None
            z_right_new_height=None
        z.right = T2val
        if z.root:
            z.root = False
            y.root = True



        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z_right_new_height))

        y_left_new_height = self.get_height_by_id(z.height)
        y.height = 1 + max(self.getHeight(y_left_new_height),
                           self.getHeight(y.right))

        y.save()
        z.save()
        # Return the new root
        return y

    def rightRotate(self, z):



        y = self.get_node_by_id(z.left)
        T3 = self.get_node_by_id(y.right)

        # Perform rotation
        y.right = z
        z.left = T3

        # Perform rotation
        if y:
            y.right = z.id
        if T3:
            T3val = T3.id
            z_right_new_height = self.get_height_by_id(T3val)
        else:
            T3val = None
            z_right_new_height =None
        z.left = T3val

        if z.root:
            z.root = False
            y.root = True

        # Update heights
        z.height = 1 + max(self.getHeight(z_right_new_height),
                           self.getHeight(z.right))

        y_right_new_height = self.get_height_by_id(z.height)
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y_right_new_height))

        # Return the new root
        y.save()
        z.save()
        return y

    def getHeight(self, root):
        if not root or (isinstance(root,int) and root  < 0):
            return 0
        root = self.get_queryset().filter(id = root).first()
        return root.height

    def get_height_by_id(self, root):
        if not root or (isinstance(root,int) and root  < 0):
            return 0
        root = self.get_queryset().filter(id = root).first()
        return root.height

    def getBalance(self, root):
        if not root or (isinstance(root,int) and root  < 0):
            return 0
        # root_left = self.get_queryset().filter(id=root.left).first()
        # root_right = self.get_queryset().filter(id=root.right)
        return self.getHeight(root.left) - self.getHeight(root.right)

    def getMinValueNode(self, root):
        if root is None or root.left is None or (isinstance(root,int) and root  < 0) or (isinstance(root.left,int) and root.left  < 0):
            return root

        return self.getMinValueNode(root.left)

    def preOrder(self, root):
        res = []
        if root:
            root_id=root.id
            res.append(root.val)
            left = self.get_node_by_id(self.get_left_by_node_id(root_id))
            right = self.get_node_by_id(self.get_right_by_node_id(root_id))
            if left:
                res = res + self.preOrder(left)
            if right:
                res = res + self.preOrder(right)

        return res
