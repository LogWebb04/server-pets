import json as js

class Account:
    def __init__(self, json, type=None):
        self.json = dict(json)

        self.type = type

        self.id = json.get("owner_id")

        self.balance = json.get("balance")

        self.items = js.loads(json.get("items")) if isinstance(json.get("items"), str) else json.get("items")
        self.settings = json.get("settings") if isinstance(json.get("settings"), str) else json.get("settings")

        self.pets = json.get("pets")
        
        self.badges = json.get("badges")
        self.keys = json.get("keys")
    
    def owner(self, bot):
        """Get the owner"""
        return bot.get_user(self.id)

    async def sort_pets(self):
        """Sorts the account's pets into their respective types"""
        pet_types = {}

        for pet in self.pets:
            if pet.type in pet_types.keys():
                pet_types[pet.type] = pet_types[pet.type] + 1
            else:
                pet_types[pet.type] = 1
        
        if "mouse" in pet_types.keys() and pet_types["mouse"] > 1:
            pet_types["mice"] = pet_types["mouse"]
            del pet_types["mouse"]

        return pet_types

    async def add_key(self, bot, key):
        keys = self.keys
        
        if self.keys:
            keys.append(key)
        else:
            keys = [key]
        
        return await bot.db.execute("UPDATE accounts SET keys = $1 WHERE owner_id = $2", keys, self.id)
    
    async def use_key(self, bot, key):
        keys = self.keys
        
        if key not in self.keys:
            return False
        
        keys.remove(key)
        
        return await bot.db.execute("UPDATE accounts SET keys = $1 WHERE owner_id = $2", keys, self.id)
    
    def to_json(self):
        json = dict(self.json)

        if json["pets"]:
            pets = []
            
            for pet in json["pets"]:
                if type(pet) == dict:
                    pets.append(pet)
                else:
                    pets.append(pet.to_json())
                    
            json["pets"] = pets

        return json

    def __repr__(self):
        return f"<Account id={self.id}, balance={self.balance}, items={self.items}, pets={self.pets}>"
    