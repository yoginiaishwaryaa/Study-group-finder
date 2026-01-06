"""
Module: Student Group Management System

Description:
This module implements a comprehensive system for managing student groups based on their academic performance and language preferences. 
The system utilizes a combination of linked lists and hash maps to efficiently organize students into groups, handle waiting lists,
and manage language and subject data.

Key Features:
- **Student Management**: Allows for the addition, removal, displaying and searching of students based on unique IDs.
- **Dynamic Grouping**: Facilitates the creation of groups based on specific criteria (e.g., number of students in each performance category: low, mid, and high).
- **Waiting Lists**: Manages students who are waiting to be assigned to a group.
- **Language and Subject Management**: Supports the registration and management of languages and subjects using hash maps, enabling quick lookups and modifications.

Core Classes:
1. **Node Classes**:
   - `WaitingListNode`: Represents a node in the waiting list for students.
   - `GroupListNode`: Represents a group containing multiple members.
   - `MemberNode`: Represents an individual student member with associated data.

2. **Linked List Classes**:
   - `Member`: Manages a linked list of member nodes.
   - `WaitingList`: Manages a linked list of waiting list nodes.
   - `Groups`: Manages multiple groups and their associated members.

3. **Hash Map Classes**:
   - `Languages`: Implements a hash map for managing available languages and associated groups.
   - `Subjects`: Implements a hash map for managing subjects and their corresponding languages.

Usage:
- The system can be instantiated and used to add students, create groups, reshuffle members between groups, and manage language and subject data. 
- This implementation provides flexibility in handling dynamic number of groups, group sizes and student performance levels.

Note: The design leverages linked lists for dynamic member management and hash maps for efficient access of groups and subjects, a waiting list is managed 
using queues implemented with linked lists, ensuring optimal performance for various operation ensuring 
"""

# Basic node structures for linked lists
import random 

class Subjects:# time complexity is O(n)
    def __init__(self, size=8):
        #time complexity is O(1)
        """
        Initializes a new Subjects instance.

        Args:
            size (int): The size of the hash table (default is 8).
        """
        self.size = size  # Size of the hash table
        self.table = [None] * size  # Hash table to store subjects
        self.number_of_subjects = 0  # Count of subjects added
        self.subject_list = {}  # Dictionary to map course codes to Languages instances

    def hash_function(self, key):
        #time complexity is O(n) 
        """
        Computes a hash value for a given course code.

        Args:
            key (str): The course code to hash.

        Returns:
            int: The index in the hash table.
        """
        return sum(ord(c) for c in str(key)) % self.size  # Sum of ASCII values modulo table size

    def add_new_subject(self, course_code):
         #time complexity is O(1)
        """
        Adds a new subject to the hash table.

        Args:
            course_code (str): The course code to add.

        Returns:
            bool: True if the subject was added, False if it already exists.
        """
        index = self.hash_function(course_code)  # Compute the hash index
        if self.table[index] is None:
            self.table[index] = []  # Initialize the bucket if it's empty
        if course_code not in self.table[index]:
            self.table[index].append(course_code)  # Add the course code to the bucket
            self.subject_list[course_code] = Languages()  # Map course code to a Languages instance
            self.number_of_subjects += 1  # Increment subject count
            return True  # Indicate success
        return False  # Indicate the subject already exists

    def remove_subject(self, course_code):
        #time complexity is O(1)
        """
        Removes a subject from the hash table.

        Args:
            course_code (str): The course code to remove.

        Returns:
            bool: True if the subject was removed, False if it did not exist.
        """
        index = self.hash_function(course_code)  # Compute the hash index
        if self.table[index] and course_code in self.table[index]:
            self.table[index].remove(course_code)  # Remove the course code from the bucket
            del self.subject_list[course_code]  # Delete the course code from the mapping
            self.number_of_subjects -= 1  # Decrement subject count
            return True  # Indicate success
        return False  # Indicate failure

    def display_all_subjects(self):
        #time complexity is O(n)
        """
        Displays all subjects stored in the hash table.

        Returns:
            list: A list of all course codes.
        """
        subjects = []  # Initialize a list to collect subjects
        for bucket in self.table:
            if bucket:
                subjects.extend(bucket)  # Add course codes from each non-empty bucket
        return subjects  # Return the complete list of subjects

    def check_subject_exists(self, course_code):
        #time complexity is O(1)

        """
        Checks if a subject exists in the hash table.

        Args:
            course_code (str): The course code to check.

        Returns:
            bool: True if the subject exists, False otherwise.
        """
        index = self.hash_function(course_code)  # Compute the hash index
        return self.table[index] is not None and course_code in self.table[index]  # Check for existence

    def is_empty(self):
        #time complexity is O(1)
        """
        Checks if the hash table is empty.

        Returns:
            bool: True if there are no subjects, False otherwise.
        """
        return self.number_of_subjects == 0  # Check if the count of subjects is zero

    def get_or_default(self, course_code, default=None):
         #time complexity is O(1)
        """
        Retrieves the Languages instance associated with a course code.

        Args:
            course_code (str): The course code to retrieve.
            default: The value to return if the course code does not exist.

        Returns:
            Languages or default: The Languages instance for the course code, or default if not found.
        """
        index = self.hash_function(course_code)  # Compute the hash index
        if self.table[index] and course_code in self.table[index]:
            return self.subject_list[course_code]  # Return the associated Languages instance
        return default  # Return the default value if the course code is not found

    def update_course_code(self, old_code, new_code):
        """
        Updates a course code, replacing the old code with a new one.

        Args:
            old_code (str): The current course code to be updated.
            new_code (str): The new course code to set.

        Returns:
            bool: True if the course code was updated, False if the operation failed.
        """
        if not self.check_subject_exists(old_code) or self.check_subject_exists(new_code):
            return False  # Return false if the old code doesn't exist or new code already exists
        
        languages = self.subject_list[old_code]  # Get the associated Languages instance
        self.remove_subject(old_code)  # Remove the old course code
        
        index = self.hash_function(new_code)  # Compute the hash index for the new code
        if self.table[index] is None:
            self.table[index] = []  # Initialize the bucket if it's empty
        self.table[index].append(new_code)  # Add the new course code to the bucket
        self.subject_list[new_code] = languages  # Map the new course code to the same Languages instance
        self.number_of_subjects += 1  # Increment subject count
        return True  # Indicate success


class Languages:#time complexity is O(n)
    def __init__(self, size=8):
        # time complexity is O(1)
        """
        Initializes a new Languages instance.

        Args:
            size (int): The size of the hash table (default is 8).
        """
        self.size = size  # Size of the hash table
        self.table = [None] * size  # Hash table to store languages
        self.language_map = {}  # Dictionary to map languages to Groups instances

    def hash_function(self, key):
        #time complexity is O(n) , n is the lenght of the key,it iterates through each character in the key to compute the sum.for loop is used 
        """
        Computes a hash value for a given key.

        Args:
            key (str): The language to hash.

        Returns:
            int: The index in the hash table.
        """
        return sum(ord(c) for c in key) % self.size  # Sum of ASCII values modulo table size

    def add_language(self, language):
        #time complexity is O(1) only table insertion
        """
        Adds a new language to the hash table.

        Args:
            language (str): The language to add.

        Returns:
            bool: True if the language was added, False if it already exists.
        """
        index = self.hash_function(language)  # Compute the hash index
        if self.table[index] is None:
            self.table[index] = []  # Initialize the bucket if it's empty
        if language not in self.table[index]:
            self.table[index].append(language)  # Add the language to the bucket
            self.language_map[language] = Groups(language)  # Map language to a Groups instance
            return True  # Indicate success
        return False  # Indicate the language already exists

    def remove_language(self, language):
        #time complexity is O(1) 
        """
        Removes a language from the hash table.

        Args:
            language (str): The language to remove.

        Returns:
            bool: True if the language was removed, False if it did not exist.
        """
        index = self.hash_function(language)  # Compute the hash index
        if self.table[index] and language in self.table[index]:
            self.table[index].remove(language)  # Remove the language from the bucket
            del self.language_map[language]  # Delete the language from the mapping
            return True  # Indicate success
        return False  # Indicate failure

    def display_all_languages(self):
        #time complexity O(n) 
        """
        Displays all languages stored in the hash table.

        Returns:
            list: A list of all languages.
        """
        languages = []  # Initialize a list to collect languages
        for bucket in self.table:
            if bucket:
                languages.extend(bucket)  # Add languages from each non-empty bucket
        return languages  # Return the complete list of languages

    def check_language_exists(self, language):
        #time complexity O(1)
        """
        Checks if a language exists in the hash table.

        Args:
            language (str): The language to check.

        Returns:
            bool: True if the language exists, False otherwise.
        """
        index = self.hash_function(language)  # Compute the hash index
        return self.table[index] is not None and language in self.table[index]  # Check for existence

    def is_empty(self):
        #time complexity is O(n)
        """
        Checks if the hash table is empty.

        Returns:
            bool: True if all buckets are empty, False otherwise.
        """
        return all(bucket is None or len(bucket) == 0 for bucket in self.table)  # Check all buckets

    def get_or_default(self, language, default=None):
         #time complexity is O(1)
        """
        Retrieves the Groups instance associated with a language.

        Args:
            language (str): The language to retrieve.
            default: The value to return if the language does not exist.

        Returns:
            Groups or default: The Groups instance for the language, or default if not found.
        """
        index = self.hash_function(language)  # Compute the hash index
        #if index after hash function exists and the corresponding language exists
        if self.table[index] and language in self.table[index]:
            return self.language_map[language]  # Return the associated Groups instance
        return default  # Return the default value if the language is not found


class WaitingList:
    # time complexity is O(n)
    def __init__(self):
        #time complexity is o(1) only assignment operation is done
        """
        Initializes a new WaitingList instance.

        This class manages a queue of students waiting to be assigned to groups.
        """
        self.head = None  # Pointer to the front of the waiting list
        self.tail = None  # Pointer to the end of the waiting list

    def is_empty(self):
        #time complexity is O(1)
        """
        Checks if the waiting list is empty.

        Returns:
            bool: True if the waiting list is empty, False otherwise.
        """
        return self.head is None  # Return True if head is None

    def enqueue(self, student_id, name, marks, preferred_language):
        #time complexity is O(1)  inserts new node at the end without any traversal
        """
        Adds a new student to the end of the waiting list.

        Args:
            student_id (int): The unique identifier for the student.
            name (str): The name of the student.
            marks (float): The academic marks of the student.
            preferred_language (str): The preferred language of the student.
        """
        new_node = WaitingListNode(student_id, name, marks, preferred_language)  # Create a new waiting list node
        if self.is_empty():
            self.head = new_node  # Set head to new node if list is empty
            self.tail = new_node  # Set tail to new node as well
        else:
            self.tail.next = new_node  # Link the new node at the end of the list
            self.tail = new_node  # Update the tail to the new node

    def dequeue(self):
        #time complexity is O(1) only updation of pointer is done without any traversal
        """
        Removes and returns the student at the front of the waiting list.

        Returns:
            WaitingListNode or None: The student node if the list is not empty, None otherwise.
        """
        if self.is_empty():
            return None  # Return None if the list is empty
        student = self.head  # Get the front student
        self.head = self.head.next  # Move head to the next student
        if self.head is None:
            self.tail = None  # If the list is now empty, set tail to None
        return student  # Return the removed student node

    def display(self):
        # time complexity is o(n) , traverse the entire queue to  print the student details
        """
        Displays the names of all students in the waiting list.

        Iterates through the list and prints the name of each student.
        """
        if self.is_empty():
            print("is Empty!")  # Print message if the list is empty
            return None
        
        student = self.head
        while student is not None:
            print(student.name)  # Print the name of the current student
            student = student.next  # Move to the next student


class WaitingListNode:# time complexity is O(1) only assignment is done in __init__ method 
    def __init__(self, student_id, name, marks, preferred_language):
        #time complexity is O(1)
        """
        Initializes a new WaitingListNode instance.

        Args:
            student_id (int): The unique identifier for the student.
            name (str): The name of the student.
            marks (float): The academic marks of the student.
            preferred_language (str): The preferred language of the student.
        """
        self.student_id = student_id  # Unique identifier for the student
        self.name = name  # Name of the student
        self.marks = marks  # Academic marks of the student
        self.preferred_language = preferred_language  # Preferred language of the student
        self.next = None  # Pointer to the next node in the waiting list


class Member:#time complexity is O(n)
    def __init__(self):
        #time complexity is O(1)
        """
        Initializes a new Member instance that manages a linked list of member nodes.
        """
        self.head = None  # Pointer to the head of the linked list
        self.number_of_members = 0  # Total number of members in the list
        self.count_low = 0  # Count of low-performing members
        self.count_mid = 0  # Count of mid-performing members
        self.count_high = 0  # Count of high-performing members

    def is_empty(self):
        #time complexity o(1) only one check the value 
        """
        Checks if the member list is empty.

        Returns:
            bool: True if the list is empty, False otherwise.
        """
        return self.head is None  # Return True if head is None

    def add_member(self, name, marks, preferred_language, student_id):
        #time complexity o(n) ,n is the no of nodes in the  linkedlist 
        """
        Adds a new member to the linked list.

        Args:
            name (str): The name of the student.
            marks (float): The academic marks of the student.
            preferred_language (str): The preferred language of the student.
            student_id (int): The unique identifier for the student.

        Returns:
            bool: True if the member was added successfully.
        """
        new_member = MemberNode(name, marks, preferred_language, student_id)  # Create a new member node
        
        if self.is_empty():
            self.head = new_member  # Set head to new member if list is empty
        else:
            current = self.head
            while current.next:  # Traverse to the end of the list
                current = current.next
            current.next = new_member  # Add the new member at the end
            
        self.number_of_members += 1  # Increment the member count
        
        # Update performance category counts
        if new_member.label == "low":
            self.count_low += 1
        elif new_member.label == "mid":
            self.count_mid += 1
        else:
            self.count_high += 1
        return True  # Return success

    def delete_member(self, student_id):
        #time complexity is o(n) , n is the no of nodes in the  linkedlist , traverse the entire list to find and delete the member
        """
        Deletes a member from the linked list by student ID.

        Args:
            student_id (int): The unique identifier for the student to be deleted.

        Returns:
            bool: True if the member was deleted successfully, False otherwise.
        """
        if self.is_empty():
            return False  # Return failure if the list is empty

        if self.head.student_id == student_id:
            # Update count based on the performance label of the head member
            if self.head.label == "low":
                self.count_low -= 1
            elif self.head.label == "mid":
                self.count_mid -= 1
            else:
                self.count_high -= 1
            self.head = self.head.next  # Remove head and update it
            self.number_of_members -= 1  # Decrement member count
            return True  # Return success

        current = self.head
        while current.next:  # Traverse the list to find the member
            if current.next.student_id == student_id:
                # Update count based on the performance label of the member being deleted
                if current.next.label == "low":
                    self.count_low -= 1
                elif current.next.label == "mid":
                    self.count_mid -= 1
                else:
                    self.count_high -= 1
                current.next = current.next.next  # Remove the member from the list
                self.number_of_members -= 1  # Decrement member count
                return True  # Return success
            current = current.next
        return False  # Return failure if the member was not found
    
    def search_member_id(self, member_id): 
        #time complexity is o(n) , n is no of nodes in linked list
        """
        Searches for a member by their unique student ID.

        Args:
            member_id (int): The unique identifier for the student.

        Returns:
            MemberNode or None: The member node if found, None otherwise.
        """
        current = self.head
        while current:
            if current.student_id == member_id:
                return current  # Return the member node if found
            current = current.next
        return None  # Return None if not found

    def display_members(self):
        #time complexity is o(n) , n is no of nodes in linked list
        """
        Displays all members in the linked list.

        Iterates through the member list and prints details of each member.
        """
        current = self.head
        while current:
            print(f"Name: {current.name}, ID: {current.student_id}, "
                  f"Marks: {current.marks}, Label: {current.label},"
                  f" Language: {current.preferred_language}")  # Print member details
            current = current.next  # Move to the next member

    def merge_members(self, mem1, mem2): #time complexity is O(n)
        '''
        
        Merging two list of members

        Args:
            mem1 (node): head of the member list of the first group
            mem2 (node): head of the member list of the second group

        Returns:
            None or list: if the conditions are satisfied and and list is formed, the list is returned else none.
        '''
        current = mem1
        a = current  # Find the end of the first list
        # Traverse to the last node of mem1
        while a.next:
            a = a.next
        a.next = mem2
        # Initialize counters for each label type
        h = 0  
        m = 0  
        l = 0 
        # Check if the merged list meets the required label distribution:
        cur = current
        while cur:
            if cur.label == "high":
                h += 1
            elif cur.label == "mid":
                m += 1
            else:
                l += 1
            cur = cur.next
        if h != 2 or m != 3 or l != 2:
            return None  # Return None condition not met
        # Return list if condition met
        return current        


class MemberNode:#time complexity is O(1)
    def __init__(self, name, marks, preferred_language, student_id):
         #time complexity is O(1)
        """
        Initializes a new MemberNode instance.

        Args:
            name (str): The name of the student.
            marks (float): The academic marks of the student.
            preferred_language (str): The preferred language of the student.
            student_id (int): The unique identifier for the student.
        """
        self.name = name  # Name of the student
        self.marks = marks  # Academic marks of the student
        self.preferred_language = preferred_language  # Preferred language of the student
        self.student_id = student_id  # Unique identifier for the student
        self.next = None  # Pointer to the next member in the list

        # Determine the performance label based on marks
        if marks < 40:
            self.label = "low"  # Label for low marks
        elif marks < 75:
            self.label = "mid"  # Label for mid-range marks
        else:
            self.label = "high"  # Label for high marks

    def update_marks(self, new_marks):
        #time cmplexity is O(1) ony assignment is done , does not depend on the input size
        """
        Updates the marks of the member and adjusts the performance label.

        Args:
            new_marks (float): The new academic marks to be set.
        """
        self.marks = new_marks  # Update the marks
        # Update the performance label based on the new marks
        if new_marks < 40:
            self.label = "low"  # Update label to low
        elif new_marks < 75:
            self.label = "mid"  # Update label to mid
        else:
            self.label = "high"  # Update label to high


class Groups:
    def __init__(self, language):
        #time complexity is O(1)
        """
        Initializes a new Groups instance.

        Args:
            language (str): The language associated with the groups.
        """
        self.language_value = language  # The language of the groups
        self.no_of_groups = 0  # Counter for the number of groups
        self.waiting_list_low = WaitingList()  # Waiting list for low scoring students
        self.waiting_list_mid = WaitingList()  # Waiting list for mid scoring students
        self.waiting_list_high = WaitingList()  # Waiting list for high scoring students
        
        self.head = None  # Pointer to the head of the group linked list
        self.tail = None  # Pointer to the tail of the group linked list

    def add_new_group(self, group_id):
        #time complexity O(1)
        """
        Adds a new group to the group management system.

        Args:
            group_id (int): The unique identifier for the new group.

        Returns:
            GroupListNode: The newly created group node.
        """
        new_group = GroupListNode(group_id)  # Create a new group node
        if not self.head:
            self.head = new_group  # Set head to new group if list is empty
            self.tail = new_group  # Set tail to new group as well
        else:
            self.tail.next = new_group  # Link the new group at the end of the list
            self.tail = new_group  # Update tail to the new group
        self.no_of_groups += 1  # Increment the group count
        return new_group  # Return the newly created group

    # Reshuffling happens only for the group with seven members (low rating)
    def reshuffle(self, group1_id, group2_id):
        #time Complexity is O(n)
        """
        Reshuffles members between two specified groups based on performance criteria.

        Args:
            group1_id (int): The ID of the first group.
            group2_id (int): The ID of the second group.

        Returns:
            tuple: A tuple containing the updated group nodes if successful, otherwise (False, None, None).
        """
        group1 = self.search_group_id(group1_id)  # Search for the first group
        group2 = self.search_group_id(group2_id)  # Search for the second group
        
        if not group1 or not group2:
            return False, None, None  # Indicate failure if either group is not found
        
        # Gather all members from both groups
        members = []
        current = group1.member_list.head
        while current:
            members.append(current)  # Append members of group 1
            current = current.next

        current = group2.member_list.head
        while current:
            members.append(current)  # Append members of group 2
            current = current.next

        print("\nCount of members being currently shuffled:", len(members))  # Print total number of members
        # Shuffle members
        random.shuffle(members)  # Shuffle the list of members
        
        # Reset member lists for both groups
        group1.member_list.head = None
        group2.member_list.head = None

        group1.member_list.number_of_members = 0
        group1.member_list.count_high=0
        group1.member_list.count_mid=0
        group1.member_list.count_low=0
        group2.member_list.number_of_members = 0
        group2.member_list.count_high=0
        group2.member_list.count_mid=0
        group2.member_list.count_low=0

        counts = {'low': 0, 'mid': 0, 'high': 0}  # Reset counts for member distribution
        member = members.pop()  # Start with a randomly selected member
        while True:
            # Distribute members to group 1 based on their labels and counts
            if member.label == 'low' and counts['low'] < 2:
                group1.member_list.add_member(
                    member.name, member.marks, 
                    member.preferred_language, member.student_id
                )
                counts['low'] += 1
            elif member.label == 'mid' and counts['mid'] < 3:
                group1.member_list.add_member(
                    member.name, member.marks, 
                    member.preferred_language, member.student_id
                )
                counts['mid'] += 1
            elif member.label == 'high' and counts['high'] < 2:
                group1.member_list.add_member(
                    member.name, member.marks, 
                    member.preferred_language, member.student_id
                )
                counts['high'] += 1
            else:
                # Assign remaining members to the second group
                if member.label == 'low' or counts['low'] >= 2:
                    group2.member_list.add_member(
                        member.name, member.marks, 
                        member.preferred_language, member.student_id
                    )
                elif member.label == 'mid' or counts['mid'] >= 3:
                    group2.member_list.add_member(
                        member.name, member.marks, 
                        member.preferred_language, member.student_id
                    )
                elif member.label == 'high' or counts['high'] >= 2:
                    group2.member_list.add_member(
                        member.name, member.marks, 
                        member.preferred_language, member.student_id
                    )
            if len(members) == 0:
                break  # Exit loop if no members left
            member = members.pop()  # Get the next member
        
        print("length of both groups: ", (group1.member_list.number_of_members), (group2.member_list.number_of_members))  # Print the number of members in both groups

        return group1, group2  # Return both updated groups

    def search_group_id(self, group_id): 
        # time complexity is O(n),traverse the group linked list
        """
        Searches for a group by its ID.

        Args:
            group_id (int): The ID of the group to search for.

        Returns:
            GroupListNode or None: The found group node or None if not found.
        """
        current = self.head  # Start at the head of the group list
        while current:
            if current.group_id == group_id:
                return current  # Return the found group
            current = current.next  # Move to the next group
        return None  # Return None if the group is not found
    
    def merge_groups(self, group_id_1, group_id_2):
        #time complexity is O(n) 
        """
        merging two groups

        Args:
            group_1 (int): The ID of the group 1 to search for.
            group_2 (int): The ID of the group 2 to search for.

        Returns:
            True or False: Whether the groups are merged or not
        """
        group1 = self.search_group_id(group_id_1) # Search for first group
        group2 = self.search_group_id(group_id_2) # Search for second group
        stu = group1.member_list.merge_members(group1.member_list.head, group2.member_list.head) # Merging group
        # If merginig is successful
        if stu: 
            group1.member_list.head = stu
            self.remove_group(group2.group_id) # Empting group 
            return True
        # If merging fails
        return False

    def create_new_group(self):
        # time complexity is O(n) n is the no of students in waiting list , each waiting list must be traversed to count the students and dequeue the members
        """
        Creates a new group based on the availability of students in waiting lists.

        Returns:
            GroupListNode or None: The newly created group if successful, None otherwise.
        """
        # Check if we have enough students in waiting lists
        high_count = 0
        mid_count = 0
        low_count = 0

        # Count students in waiting lists
        temp = self.waiting_list_high.head
        while temp:
            high_count += 1
            temp = temp.next

        temp = self.waiting_list_mid.head
        while temp:
            mid_count += 1
            temp = temp.next

        temp = self.waiting_list_low.head
        while temp:
            low_count += 1
            temp = temp.next

        # Try to find an existing empty group
        empty_group = None
        current = self.head
        while current:
            if current.member_list.is_empty():  # Check if the group is empty
                empty_group = current  # Assign the empty group
                break
            current = current.next

        # Check if we have enough students to form a valid group
        if high_count >= 2 and mid_count >= 3 and low_count >= 2:
            # If there is an empty group, use it
            if empty_group:
                new_group = empty_group  # Reuse the empty group
                print(f"Using existing empty group: {empty_group.group_id}")
            else:
                # Check if we can form a valid group of exactly 7 members
                new_group = self.add_new_group(self.no_of_groups + 1)  # Create a new group

            # Add high scoring students (2)
            for _ in range(2):
                student = self.waiting_list_high.dequeue()  # Dequeue a student from the high list
                new_group.member_list.add_member(
                    student.name, student.marks, 
                    student.preferred_language, student.student_id
                )

            # Add mid scoring students (3)
            for _ in range(3):
                student = self.waiting_list_mid.dequeue()  # Dequeue a student from the mid list
                new_group.member_list.add_member(
                    student.name, student.marks, 
                    student.preferred_language, student.student_id
                )

            # Add low scoring students (2)
            for _ in range(2):
                student = self.waiting_list_low.dequeue()  # Dequeue a student from the low list
                new_group.member_list.add_member(
                    student.name, student.marks, 
                    student.preferred_language, student.student_id
                )

            # Ensure exactly 7 members
            if new_group.member_list.number_of_members != 7:
                # If the group does not have exactly 7 members, reset the group
                self.no_of_groups -= 1
                return None

            return new_group  # Return the newly created group

        return None  # Not enough students to create a valid group

    def remove_group(self, group_id):
        # time complexity is o(n), n is the no of groups and entire linked list is traversed to fing the target groups
        """
        Removes a group by its ID and resets its member list.

        Args:
            group_id (int): The ID of the group to remove.

        Returns:
            bool: True if the group was successfully removed, False otherwise.
        """
        current = self.head  # Start at the head of the group list
        while current:
            if current.group_id == group_id:
                current.member_list.head = None  # Clear the member list
                current.member_list.number_of_members = 0  # Reset member count
                current.member_list.count_low = 0  # Reset low count
                current.member_list.count_mid = 0  # Reset mid count
                current.member_list.count_high = 0  # Reset high count
                return True  # Indicate success
            current = current.next  # Move to the next group
        return False  # Return False if the group was not found
    
    # time complexity is O(n) , n is the no of groups , traverse whole list and displays the groups ids
    def display_groups_ids(self):
        """
        Displays the IDs of all groups in the group management system.

        Iterates through the group list and prints the ID of each group.
        """
        current = self.head  # Start at the head of the group list
        print("Current groups:", self.language_value)
        while current:
            print(f"Group ID: {current.group_id}")  # Print the group ID
            current = current.next  # Move to the next group

    def delete_member(self, group_id, member_id):
    ################################################################################# time complexity 
        """
        Removes a specific member from a study group 
        
        Args:
            group_id (int): The ID of the group to remove.
            member_id (int): The ID of member
        """
        group = self.search_group_id(group_id)

        label = group.member_list.search_member_id(member_id).label
        if label == "high":
            student = self.waiting_list_high.dequeue()         
        elif label=="mid":
            student = self.waiting_list_mid.dequeue() 
        else:
            student = self.waiting_list_low.dequeue() 
        
        if student:
            group.member_list.add_member(
                        student.name, student.marks, 
                        student.preferred_language, student.student_id
                    ) #add student Arun
        group.member_list.delete_member(member_id)

        self.possible_merging()

    def possible_merging(self): 
        #time Complexity O(n^2)   

        """
        merges 2 compatible groups when they have less than 7 members

        """

        l = self.classify_groups()
        li = l[1]
        current = self.head  # Start at the head of the group list
        while current:
            if current.group_id not in li:
                curr = self.head
                while curr and curr!=current:
                    if ((curr.member_list.count_high + curr.member_list.count_high)+(curr.member_list.count_mid + curr.member_list.count_mid)+(curr.member_list.count_low + curr.member_list.count_low))==7:
                        self.merge_groups(current.group_id, curr.group_id)
                    curr = curr.next
            current = current.next
            
    def classify_groups(self):
        #time complexity is O(n)

        """
        Classifies the groups into two categories based on the number of members each group contains.

        Returns:
            A tuple containing two lists:
                - L1: A list of GroupListNode objects representing groups with exactly seven members.
                - L2: A list of GroupListNode objects representing groups with fewer than seven members.
        """

        # Initialize two lists to hold the classified groups
        L1=[]
        L2=[]
        current = self.head  # Start with the head of the linked list
        while current:
            if current.member_list.number_of_members==7:
                L1.append(current) # Add to L1 if there are 7 members
            else:
                L2.append(current)  # Add to L2 for all other member counts
            current = current.next
        return (L1,L2)
    
    #24/7 condition check
    def condition_checker(self):
        #time complexity is O(n^2)

        """
        Orchestrates the classification of groups, assesses their performance, and executes reshuffling and removal operations 
        based on predefined criteria.

        """
        _2d=(self.classify_groups())
        L1=_2d[0] # Extract the list of groups with exactly 7 members
        L=[] # for storing groups to reshuffle

        
        for group in L1:
             # Check if the member distribution does not match the expected counts
            if (group.member_list.count_high!=2 or group.member_list.count_mid!=3 or group.member_list.count_low!=2):
                if group.calc_avg_rating()<2:
                    self.remove_group(group.group_id)
                    
            else:
                # If the member distribution is correct, check average rating
                if group.calc_avg_rating()<2:
                    L.append(group)
                # Reshuffle groups

        for i in range(len(L)-1):
            res=self.reshuffle(L[i].group_id,L[(i+1)].group_id)
            if res:
                L[i],L[i+1]=res  
        if L[0]!=L[-1]:                
            res=self.reshuffle(L[-1].group_id,L[0].group_id)
            if res:
                L[-1],L[0]=res
        
        #checking merging
        self.possible_merging()


class GroupListNode:# time complexity is O(n)
    def __init__(self, group_id):
        #time complexity is O(1)
        """
        Initializes a new GroupListNode instance.

        Args:
            group_id (int): The unique identifier for the group.
        """
        self.group_id = group_id  # Unique identifier for the group
        self.next = None  # Pointer to the next node in the group list
        self.member_list = Member()  # Linked list to manage group members
        self.session_rating = []  # List to store session ratings for the group
        self.count_low = 0  # Count of low-performing members
        self.count_mid = 0  # Count of mid-performing members
        self.count_high = 0  # Count of high-performing members
        self.is_custom = False  # Flag indicating if the group is custom-created
        self.number_of_members = 0  # Total number of members in the group
        
    def calc_avg_rating(self):
            #time complexity is o(n) n is the no of ratings , one for loop is used so o(n)
        """
        Calculates the average rating of the group based on session ratings.


        Returns:
            float: The average session rating of the group.
        """
        sum = 0  # Initialize sum of ratings
        for rating in self.session_rating:  # Iterate through session ratings
            sum += rating  # Accumulate ratings
        avg = sum / len(self.session_rating) if self.session_rating else 0  # Calculate average
        return avg  # Return the average rating
            
    def display_members(self):
        #time complexity is o(n) n is the no of members , method is called n times to display all the members
        """
        Displays the members of the group.

        Calls the display_members method of the member_list to show all members.
        """
        self.member_list.display_members()  # Display all members in the group


#Driver class
class StudyGroupFinderDriver:
    def run_tests(self):
        print("Starting Study Group Finder Tests...")
        
        # Test Subject Management
        subjects = Subjects()
        print("\n1. Testing Subject Management:")
        print("Adding subjects...")
        subjects.add_new_subject("CS101")
        subjects.add_new_subject("CS102")
        print("Current Subjects:", subjects.display_all_subjects())

        #check_subject_exists(self, course_code)
        print("CS102 exists in Subjects:",subjects.check_subject_exists("CS102"))
            

        # Test Language Management
        print("\n2. Testing Language Management:")
        cs101_languages = subjects.get_or_default("CS101")
        cs101_languages.add_language("English")
        cs101_languages.add_language("Hindi")
        cs101_languages.add_language("Tamil")
        print("Languages for CS101:", cs101_languages.display_all_languages())  

        '''Additional testing'''
        #.......removing a language.......
        #cs101_languages.remove_language("Tamil")
        #print("Languages for CS101:", cs101_languages.display_all_languages())

        #.........checking for language.......
        #print(cs101_languages.check_language_exists("Tamil"))

        #........update course........
        #print("\nupdate\n")
        #subjects.update_course_code("CS101","EC234")
        #print("Subjects:", subjects.display_all_subjects())

        #............checking whether the languages have been copied.........
        #print("languages are copied or not? ")
        #print(subjects.get_or_default("EC234").display_all_languages())


        #.........Test Group Creation and Member Management...........

        #........get_or_default..........
        print("\n3. Testing Group and Member Management:")
        english_groups = cs101_languages.get_or_default("English")
        tamil_groups = cs101_languages.get_or_default("Tamil")
        
        #............Add students to waiting lists..........
        '''if inputs is being taken from user, use if conditions'''

        print("Adding students to English waiting lists...")    

        #.........High scoring students - english..........
        english_groups.waiting_list_high.enqueue(1, "Amanada", 85, "English")
        english_groups.waiting_list_high.enqueue(2, "Bethany", 90, "English")
        
        #.........High scoring students - tamil...........
        tamil_groups.waiting_list_high.enqueue(3, "Catherine", 100, "Tamil")
        
        
        #............Mid scoring students.............
        english_groups.waiting_list_mid.enqueue(4, "Deborah", 65, "English")
        english_groups.waiting_list_mid.enqueue(5, "Emma", 70, "English")
        english_groups.waiting_list_mid.enqueue(6, "Yogini", 45, "English")
 
        
        #..............Low scoring students............
        english_groups.waiting_list_low.enqueue(7, "Fathima", 30, "English")
        english_groups.waiting_list_low.enqueue(8, "Geetha", 30, "English")
        english_groups.waiting_list_low.enqueue(9, "Hannah", 30, "English")
        
        print("Low scoring waiting list: ")
        english_groups.waiting_list_low.display()
        print("\nMid scoring waiting list: ")
        english_groups.waiting_list_mid.display()
        print("\nHigh scoring waiting list: ")
        english_groups.waiting_list_high.display()
        print("\ntamil\nHigh scoring waiting list: ")
        tamil_groups.waiting_list_high.display()
        print("\n")


        print("Adding more students to waiting list...")        
        #...........group 2 test case.............
        english_groups.waiting_list_high.enqueue(10, "Devika", 90, "English")
        english_groups.waiting_list_high.enqueue(11, "Alex", 85, "English")
        english_groups.waiting_list_mid.enqueue(12, "Sarah", 70, "English")
        english_groups.waiting_list_mid.enqueue(13, "Michael", 60, "English")
        english_groups.waiting_list_mid.enqueue(14, "Ignacio", 60, "English")
        english_groups.waiting_list_mid.enqueue(15, "Jordan", 60, "English")
        english_groups.waiting_list_mid.enqueue(16, "Kris", 60, "English")
        english_groups.waiting_list_low.enqueue(17, "Bartholomew", 30, "English")
        
        #...........group 3 test case - when slot is empty..........
        english_groups.waiting_list_high.enqueue(18, "Isabel", 90, "English")
        english_groups.waiting_list_high.enqueue(19, "Max", 85, "English")
        english_groups.waiting_list_mid.enqueue(20, "Selena", 70, "English")
        english_groups.waiting_list_mid.enqueue(21, "Jessie", 60, "English")
        english_groups.waiting_list_mid.enqueue(22, "Betty", 60, "English")
        english_groups.waiting_list_mid.enqueue(23, "Sam", 60, "English")
        english_groups.waiting_list_mid.enqueue(24, "Dokyeom", 60, "English")
        english_groups.waiting_list_low.enqueue(25, "Yelena", 30, "English")
        english_groups.waiting_list_high.enqueue(26, "Lalitha", 85, "English")
        english_groups.waiting_list_mid.enqueue(27, "Tessa", 70, "English")
        english_groups.waiting_list_mid.enqueue(28, "Cassandra", 60, "English")
        english_groups.waiting_list_mid.enqueue(29, "David", 60, "English")
        english_groups.waiting_list_low.enqueue(30, "Chiara", 30, "English")
       
        print("\nLow scoring waiting list: ")
        english_groups.waiting_list_low.display()
        print("\nMid scoring waiting list: ")
        english_groups.waiting_list_mid.display()
        print("\nHigh scoring waiting list: ")
        english_groups.waiting_list_high.display()
        

        #..........Create a new group 1.............
        print("\nCreating new group (group-1)...")
        new_group1 = english_groups.create_new_group()
        if new_group1:
            print("Group created successfully!")
            print("\nGroup members:")
            new_group1.member_list.display_members()

      
        #..........Create a new group 2............
        print("\nCreating new group (group-2)...")
        new_group2 = english_groups.create_new_group()
        if new_group2:
            print("Group created successfully!")
            print("\nGroup members:")
            new_group2.member_list.display_members()
            

        #...........creating a new group 3.............
        print("\nCreating new group (group-3)...")
        new_group = english_groups.create_new_group()
        if new_group:
            print("Group created successfully!")
            print("\nGroup members:")
            new_group.member_list.display_members()


        #........checking multi-level and displaying........
        print("\nMulti-level key lookup: ")
        print("(Key Advantage of nested HashMap:)")
        subjects.get_or_default("CS101").get_or_default("English").display_groups_ids()
      

        #....printing the number of groups........
        print("\nNo. of english groups: ")
        print(english_groups.no_of_groups)
       
        
        #..........merging when 2 groups do not have enough members and the waiting list is empty..........
        #deleting group 1 members
        english_groups.search_group_id(1).member_list.delete_member(1)
        english_groups.search_group_id(1).member_list.delete_member(2)
        english_groups.search_group_id(1).member_list.delete_member(4)
        #...remaining (5, 6, 7, 8)
        #deleting group 2 members
        english_groups.search_group_id(2).member_list.delete_member(13)
        english_groups.search_group_id(2).member_list.delete_member(14)
        english_groups.search_group_id(2).member_list.delete_member(9)
        english_groups.search_group_id(2).member_list.delete_member(17)
        #remaining (10, 11, 12)


        #...........Test split_list() method ............
        print("debugging split_list()")
        L=english_groups.classify_groups()
        L1=L[0]
        L2=L[1]
        print(f"number of groups having length=7: {len(L1)}\nnumber of groups not having length=7:  {len(L2)}")
       

        #.......the main method, running for 24/7...........
        english_groups.condition_checker()


        #.........merging........
        english_groups.merge_groups(1, 2)

        print("\nAfter merging...")
        print("\nGroup 1:")
        english_groups.search_group_id(1).display_members()
        print("\nGroup 2:")
        english_groups.search_group_id(2).display_members()
        print("\nGroup 3:")
        english_groups.search_group_id(3).display_members()


        ########test case - inserting###########
        english_groups.waiting_list_high.enqueue(1, "Amanada", 85, "English")
        english_groups.waiting_list_high.enqueue(2, "Bethany", 90, "English")
        english_groups.waiting_list_mid.enqueue(4, "Deborah", 65, "English")
        english_groups.waiting_list_low.enqueue(9, "Hannah", 30, "English")
        english_groups.waiting_list_mid.enqueue(13, "Michael", 60, "English")
        english_groups.waiting_list_mid.enqueue(14, "Ignacio", 60, "English")
        english_groups.waiting_list_low.enqueue(17, "Bartholomew", 30, "English")


        print("\nCreating new group...")
        new_groupp = english_groups.create_new_group()
        if new_groupp:
            print("Group created successfully!")
            print("\nGroup members:")
            new_groupp.member_list.display_members()
        ########################################


        #######present groups and members#########
        print("\nGroup 1:")
        english_groups.search_group_id(1).display_members()
        print("\nGroup 2:")
        english_groups.search_group_id(2).display_members()
        print("\nGroup 3:")
        english_groups.search_group_id(3).display_members()
        ########################################

        

        #..........updating sessions........          
        print("\n4. Testing Group Ratings......")

        if new_group: #first group
                new_group.session_rating.append(1.5)
                new_group.session_rating.append(1.8)
                print("Session ratings:", new_group.session_rating)

        if new_group1: #second group
            new_group1.session_rating.append(1)
            new_group1.session_rating.append(1.2)
            print("Session ratings:", new_group1.session_rating)
            
        if new_group2: #third group
            new_group2.session_rating.append(1)
            new_group2.session_rating.append(1)
            print("Session ratings:", new_group2.session_rating)
            


        #.........calling reshuffle on groups whose avg rating < 2......
        print("\nBefore shuffling...........\n")
        english_groups.display_groups_ids()
        print("\ngroup 1:")
        english_groups.search_group_id(1).display_members()
        print("\ngroup 2:")
        english_groups.search_group_id(2).display_members()
        print("\ngroup 3:")
        english_groups.search_group_id(3).display_members()

        head=english_groups.head
        L=[]
        temp=head
        while temp:
            if temp.calc_avg_rating()<2:
                L.append(temp)
            temp=temp.next
            
        for i in range(len(L)-1):
            res=english_groups.reshuffle(L[i].group_id,L[(i+1)].group_id)
            if res:
                L[i],L[i+1]=res
        if L[0]!=L[-1]:                
            res=english_groups.reshuffle(L[-1].group_id,L[0].group_id)
            if res:
                L[-1],L[0]=res
      
        print("\nAfter shuffling............\n")
        english_groups.display_groups_ids()
        print("\ngroup 1:")
        english_groups.search_group_id(1).display_members()
        print("\ngroup 2:")
        english_groups.search_group_id(2).display_members()
        print("\ngroup 3:")
        english_groups.search_group_id(3).display_members()
      


        #.........Reshuffle groups with ID 1 and 2.......
        '''print("\nReshuffling groups...")
        new_group1, new_group2 = english_groups.reshuffle(1, 2)

        if new_group1:
            print("New Group 1 Members:")
            new_group1.member_list.display_members()
        else:
            print("New Group 1 could not be created.")

        if new_group2:
            print("New Group 2 Members:")
            new_group2.member_list.display_members()
        else:
            print("New Group 2 could not be created.")'''
        
        

        #............Test removing a group..............
        print("\n5. Removing group...")
        if english_groups.remove_group(1):  # Assuming group ID is 1
            print("Group 1 removed successfully!")
        else:
            print("Failed to remove Group 1.")
        
        if new_group1:
            print("\nGroup 1 members after removal:")
            new_group1.member_list.display_members()  # Should show no members
        
        

        #.......Displaying remaining groups and their members............
        print("\nRemaining groups:")
        english_groups.display_groups_ids()
        print("\nGroup 1: ")
        english_groups.search_group_id(1).display_members() #empty
        print("\n Group 2: ")
        english_groups.search_group_id(2).display_members()
        print("\n Group 3: ")
        english_groups.search_group_id(3).display_members()
        
            
        #........make new group.........
        print("\nChecking for new group...")
        new_group = english_groups.create_new_group()
        if new_group:
            print("Group created successfully!")
            print("\nGroup members:")
            new_group.member_list.display_members()
            
        print("Check if group-1 is empty: ", end = " ")
        print(english_groups.search_group_id(1).member_list.is_empty())


        
        #.........test if new grp gets entered into group 1........
        english_groups.waiting_list_high.enqueue(31, "Senthil", 90, "English")
        english_groups.waiting_list_high.enqueue(32, "Arun", 85, "English")
        english_groups.waiting_list_mid.enqueue(33, "Kumar", 70, "English")
        english_groups.waiting_list_mid.enqueue(34, "Karan", 60, "English")
        english_groups.waiting_list_mid.enqueue(35, "Thea", 60, "English")
        english_groups.waiting_list_mid.enqueue(36, "Mary", 60, "English")
        english_groups.waiting_list_mid.enqueue(37, "Sriya", 60, "English")
        english_groups.waiting_list_low.enqueue(38, "Stella", 30, "English")
        english_groups.waiting_list_low.enqueue(39, "Markus", 30, "English")

        new_group = english_groups.create_new_group()
        if new_group:
            print("\nNew group is created")
        
        english_groups.display_groups_ids()
        print("\nGroup 1:")
        english_groups.search_group_id(1).display_members()
        print("\nGroup 2:")
        english_groups.search_group_id(2).display_members()
        print("\nGroup 3:")
        english_groups.search_group_id(3).display_members()
        

        
        #.....when a member leaves, replace it with someone from waiting list.....
        print("before........")
        english_groups.search_group_id(1).display_members()
        english_groups.delete_member(1, 2)
        print("\n..Updated group after a member left and new one is added 1:")
        english_groups.search_group_id(1).display_members()


        #.........updating marks........
        stu = english_groups.search_group_id(1).member_list.search_member_id(39) #in the group-1, Markus
        stu.update_marks(79)
        print("\nAfter updating the marks of id 39(Markus): ")
        english_groups.search_group_id(1).display_members()
        


        #...........reshuffling after updating, default conditions are not maintained............
        print("\nBefore shuffling....")
        english_groups.display_groups_ids()
        print("\ngroup 1:") #stays as it is because the count value is violated so it stays as a "unchanged group"
        english_groups.search_group_id(1).display_members()
        print("\ngroup 2:")
        english_groups.search_group_id(2).display_members()
        print("\ngroup 3:")
        english_groups.search_group_id(3).display_members()

                
        #..........calling reshuffle on groups whose avg rating < 2..............        
        head=english_groups.head
        L=[]
        temp=head
        while temp:
            if temp.calc_avg_rating()<2:
                L.append(temp)
            temp=temp.next
            
        for i in range(len(L)-1):
            res=english_groups.reshuffle(L[i].group_id,L[(i+1)].group_id)
            if res:
                L[i],L[i+1]=res                  
        if L[0]!=L[-1]:                
            res=english_groups.reshuffle(L[-1].group_id,L[0].group_id)
            if res:
                L[-1],L[0]=res
      
        print("\nAfter shuffling..........")
        english_groups.display_groups_ids()
        print("\nGroup 1:")
        english_groups.search_group_id(1).display_members()
        print("\nGroup 2:")
        english_groups.search_group_id(2).display_members()
        print("\nGroup 3:")
        english_groups.search_group_id(3).display_members()
        

if __name__ == '__main__':
    StudyGroupFinderDriver().run_tests()