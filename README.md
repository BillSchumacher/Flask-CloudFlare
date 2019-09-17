Flask-CloudFlare
============

Provides a Flask Extension to interact with the CloudFlare Workers KV service.

In the future it will support more API endpoints with CloudFlare.

This project is not affiliated with CloudFlare in any way and CloudFlare and associated copyrights belong to CloudFlare.

Usage
--

This is just a wrapper, ideally it will pass along attributes to the underlying pycflare class.

    from flask_cloudflare import CloudFlare, cloudflare
    from flask import Flask
    
    # The lowercase cloudflare is a proxy to the current app's CloudFlare extension.
    
    account_id = "YOUR_CLOUDFLARE_ACCOUNT_ID"
    
    cf = CloudFlare()
    app = Flask(__name__)
    app.config['CLOUDFLARE_AUTH_EMAIL'] = "YOUR_CLOUDFLARE_AUTH_EMAIL"
    app.config['CLOUDFLARE_AUTH_KEY'] = "YOUR_CLOUDFLARE_AUTH_KEY"
    
    cf.init_app(app)
    cf.register_account(account_id, "test")
    
    # Just generating some test data.
    new_namespace = cf.test.create_namespace("test")  # This will return None if the namespace exists.
    if new_namespace is not None:
        new_namespace.write("hello", "world")
    else:
        namespaces = cf.test.get_namespaces()
        for namespace in namespaces:
            if namespace.title == "test":
                namespace.write("hello", "world")
    
    
    @app.route("/")
    def index():
        _namespaces = cloudflare.test.get_namespaces()
        for _namespace in _namespaces:
            if _namespace.title == "test":
                hello = _namespace.get("hello")
                return "Hello, {}!".format(str(hello.value.decode('utf8')))
        # If you know the namespace ID you can also do:
        # hello = cloudflare.test.get_key(namespace_id, "hello")
        # or use the object created later assuming it is imported
        # hello = cloudflare.test.get_key(new_namespace.id, "hello")
        # hello = new_namespace.get("hello")
        return "Didn't find world!"
    
    app.run()

        
How to use pycflare:

    from pycflare import CloudFlare
    
    # I would recommend using environmental variables or 
    # some other method that does not hard-code your secrets.
    auth_email = "YOUR_CLOUDFLARE_AUTH_EMAIL"
    auth_key = "YOUR_CLOUDFLARE_AUTH_KEY"
    account_id = "YOUR_CLOUDFLARE_ACCOUNT_ID"
    
    cf = CloudFlare(auth_email, auth_key)
    
    #
    # With wrapped helpers
    #
    
    # This assigns a attribute of .test to the CloudFlare class.
    # Accounts are still cached in the .accounts attribute when accessed, if you don't register.
    
    cf.register_account(account_id, "test")
    
    # Get all Namespaces
    namespaces = cf.test.get_namespaces()
    
    # Create a new Namespace
    new_namespace = cf.test.create_namespace("test")
    
    # Write Key-Value
    cf.test.write_key(new_namespace.id, "hello", "world")
    # or
    new_namespace.write_key("hello", "world")
    # or
    new_namespace.write("hello", "world")
    
    
    # Get Key-Value
    print(cf.test.get_key(new_namespace.id, "hello"))
    # or
    print(new_namespace.get_key("hello"))
    # or
    print(new_namespace.get("hello"))
    
    
    # Iterate over keys in Namespace
    keys = cf.test.namespace_keys(new_namespace.id)
    # or
    keys = new_namespace.namespace_keys()
    # or
    keys = new_namespace.keys()
    
    print(keys)
    for key in keys:
        print(cf.test.get_key(new_namespace.id, key))
        # or
        print(new_namespace.get_key(key))
        # or
        print(new_namespace.get(key))
        
        
    # Delete a key
    cf.test.delete_key(new_namespace.id, "hello")
    # or
    new_namespace.delete_key("hello")
    # or
    hello_world = new_namespace.get("hello")
    hello_world.delete()
    
    # Renaming a Namespace
    cf.test.rename_namespace(new_namespace.id, "new_test")
    # or
    new_namespace.rename_namespace("new_test")
    # or
    new_namespace.rename("new_test")
    
    
    # Iterating over Namespaces
    namespaces = cf.test.get_namespaces()
    for namespace in namespaces:
        print(namespace)
        
    
    # Bulk Writes
    cf.test.bulk_write(new_namespace.id,
                       [{"key": "world", "value": "hello"},
                        {"key": "jello", "value": "mold"}])
    # or
    new_namespace.bulk_write([{"key": "world", "value": "hello"}, {"key": "jello", "value": "mold"}])
    
    
    # Bulk Deletes
    cf.test.bulk_delete(new_namespace.id, ["jello", "world"])
    # or
    new_namespace.bulk_delete(["jello", "world"])
    
    
    # Delete a Namespace
    cf.test.delete_namespace(new_namespace.id)
    # or
    new_namespace.delete_namespace()
    
    
    #
    # The long way, avoids a few function calls at the expense of verbosity.
    #
    
    
    # Get all Namespaces
    namespaces = cf.storage.get_namespaces(account_id)
    ## cf.storage can also be cf.kv.get_namespaces(account_id)
    
    # Create a new Namespace
    new_namespace = cf.storage.create_namespace(accound_id, "test")
    
    # Write Key-Value
    cf.storage.write_key(account_id, new_namespace.id, "hello", "world")
    
    # Get Key-Value
    print(cf.storage.get_key(account_id, new_namespace.id, "hello"))
    
    # Iterate over keys in Namespace
    keys = cf.storage.namespace_keys(account_id, new_namespace.id)
    print(keys)
    for key in keys:
        print(cf.storage.get_key(account_id, new_namespace.id, key))
        
    # Delete a key
    cf.storage.delete_key(account_id, new_namespace.id, "hello")
    
    # Renaming a Namespace
    cf.storage.rename_namespace(account_id, new_namespace.id, "new_test"))
    
    # Iterating over Namespaces
    namespaces = cf.storage.get_namespaces(account_id)
    for namespace in namespaces:
        print(namespace)
        
    # Bulk Writes
    cf.storage.bulk_write(account_id, new_namespace.id,
                          [{"key": "world", "value": "hello"},
                           {"key": "jello", "value": "mold"}])
    
    # Bulk Deletes
    cf.storage.bulk_delete(account_id, new_namespace.id, ["jello", "world"])
    
    # Delete a Namespace
    cf.storage.delete_namespace(account_id, new_namespace.id)
    


Of course you could always assign the account to a variable and avoid using the built-in attribute as well.

You also have a reference to the previous classes as you go from Account -> Namespace -> Key.

So you can do things like new_key.account or new_namespace.account or new_key.namespace, etc.

There's also a reference to the base CloudFlare class .cf which is available everywhere.


Contributing
---

* Keep it simple. 

* Don't make breaking changes, like ever.

* Submit a pull request.

Issues
---

This will be maintained for as long as I am using CloudFlare, don't hesitate to open an issue.

Roadmap
---

* Adding support for cache API.
* Adding support for routes API.
* Adding support for DNS API.

Suggestions are welcome.

License
---

Copyright (C) 2019 by Bill Schumacher

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.