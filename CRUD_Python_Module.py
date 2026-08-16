# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = username
        PASS = password 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
            
    """
        Insert a record into the database
        
        Parameters:
            data(Dict): A dictionary containing the properties and values to insert.
            
        Returns:
            bool: Whether the insertion was successful.
    """
    def create(self, data) -> bool:
        if data is not None: 
            try:
                insertionResult = self.database.animals.insert_one(data)  # data should be dictionary
                return insertionResult.acknowledged # Returns boolean whether the operation was successful
            except Exception as e:
                print(f"An error occured while inserting the entry: {e}")
                return False
        else: 
            print("Nothing to save, because data parameter is empty")
            return False

    """
        Gets full animal collection or subset of it filtered by the lookup
        
        Parameters:
        lookup(Dict): A key/value pair for filtering the search.
        
        Returns:
        List: The dataset matching the lookup or an empty list of unsuccessful
        or if there is valid data.
    """
    def read(self, lookup=None) -> list:
        # If a valid argument for filtering is provided
        # Then, use that to find out the result
        result = None
        try:
            if lookup is not None:
                result = self.database.animals.find(lookup)
            else:
                # If no lookup is provided then search for any matches
                result = self.database.animals.find({})
        except Exception as e:
            print(f"An error occurred: {e}")
        
        
        # Only return the result if it not empty
        if result is not None:
            return list(result) # Since result is cursor by default, we need to cast it to a list.
        return [] # If the result is None, return an empty list
    
    """
    Update an animal collection with given values, for the given lookup

    Remarks:
    Updates all database entry with matching lookup.

    Parameters:
    lookup(Dict): A key/value pair for filtering the search.
    updated_entry(Dict): A key/value pair for update the filtered queries.

    Returns:
    List: The number of updated collections
    """
    def update(self, lookup, updated_entry) -> int:
        # Update only proceeds if a valid lookup and entry is provided
        result = None
        try:
            if lookup is not None and updated_entry is not None:
                result = self.database.animals.update_many(lookup, {"$set": updated_entry})
            else:
                print("Lookup and updatedEntry must be provided for updating an entry!")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Only return the result if it not empty
        if result is not None:
            return result.modified_count # If update is successful, return the number of updated collections
        return 0 # If the result is None, return 0 indicating no collections were updated

    """
    Deletes an animal collection with the given lookup

    Remarks:
    Deletes all daatabase entry with matching lookup.

    Parameters:
    lookup(Dict): A key/value pair for filtering the delete operation.

    Returns:
    List: The number of deleted collections
    """
    def delete(self, lookup) -> int:
        # Delete only proceeds if a valid lookup is provided
        result = None
        try:
            if lookup is not None:
                result = self.database.animals.delete_many(lookup)
            else:
                print("Lookup query must be provided for deletion!")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Only return the result if it not empty
        if result is not None:
            return result.deleted_count # If deletion is successful, return the number of deleted collections
        return 0 # If the result is None, return 0 indicating no collections were deleted
