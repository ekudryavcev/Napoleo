# Napoleo
Project Napoleo gives a new life to data storage!

While the popular XML is rather complicated, OUI, the Napoleo syntax, allows you to get along with this project in a couple of minutes. Here's what it includes:

First line should start with the version of syntax:

(napoleoversion)(2.5.2)

The file should not be of a later version than the Napoleo compiler, but may be of an earlier one.

Now, let us create a block:

(Main){
}

We now have an empty block named "Main".
Let's add the first value field:

(Main){
  (field1)(57)
}

Main now contains a value named "field", equal to 57.
You may define values as strings, like shown above, blocks, like "Main" in this example, or lists:

(Main){
  (mylist)(three values here)
  //A commentary
  /**A block commentary. 
  Commentaries are ignored by the compiler.
  Thus, they don't need indents and can contain almost anything: 
 %^#&(@), etc. The following will close this commentary. **/
}

In fact, nothing really needs indents in Napoleo.
Actually, this is pretty much all you need to know for working with Napoleo!

Another useful feature is placing flags:

(Main){
  <anything>
}

When a value cannot be defined by some category, for example, in case it does not belong to all the objects of you data file, it is better to save this value as a flag. You may define an unlimited ammount of flags for any block.

NB: you will need Parser 1.6.6 to run Napoleo precompiling parser.
After you finished editing your file, save it with a *.oui extension.
Now let's see how to operate with your new Oui file.

In your Python 3 code import Napoleo:

from Oui import NAPOLEO

You may use the import all operation:

from Oui import *

However, you will most likely only need the NAPOLEO class.
First of all, you should create a new NAPOLEO object:

example = NAPOLEO(source, precompile, note)

Now, this is important: you have to define the location of your Oui file, like "E:\\Napoleo\\Example.oui" (for Windows; file directory would look different on Mac and Linux). 
The second argument is optional: this is the directory of a *.cdf compiled file, which by defauld would have the name and directory of your Oui file. 
The third argument is not necessary as well. It indicates special types of creating a Napoleo object. "update" would scan the *.cdf precompiled file instead of *.oui, while "empty" would create an empty object with no data. By default the Napoleo object you create precompiles the *.oui file immediately. This means it makes a *.cdf file, which is uneasy to edit,yet takes less memory and is operated much faster. Also, all your data is now saved in the "tree" field of your Napoleo object.

Here's how it can be accessed:


from Oui import *
example = NAPOLEO(source, precompile, note)
value = example.get("Main.field1")
flag0 = example.tree[Main[flags]][0]

get(...) allows to quickly reach the value or block by path - keys, divided py dots.
In some cases reading the tree directly may be useful - the tree of Napoleo is a dictionery, containing other dictionaries etc.

Napoleo objects also have such attributes as name and version.
