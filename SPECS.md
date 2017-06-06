# SPECS : 

* __GET /__ -> index of the website

## Article management
* __GET / articles / {id}__ -> webpage of the article {id}
* __POST / articles__ -> Creates a new article
```
    {
        name: string
        text: string
        author: string
		tags: array of strings
		replies_to: array of article ids
    }
```
* __PUT / articles / {id}__ -> Updates the article {id}
```
    {
		title: string,
        content: string
    } 
```
	both are optional, will remain unchanged if left out
* __DELETE / articles / {id}__ -> Deletes the article {id} (requires a current session)

## Article lists

* __GET / articles__ -> webpage with a list of articles
* __GET / articles / {oldest} | {newest} | {controversial} / ( {count} / ( {start} ) )__\\
    -> list of articles sorted by oldest, newest, controversial... \\
	Optional count of articles to return and optional starting position (Paging)

* __GET / articles / {parents_of} | {children_of} | {tagged} / {origin} / ( {count} / ( {start} ) )__
    -> list of articles that are replied to by a given article, reply to a given article or have a given tag. \\
	{origin} contains either the given article (in the case of parent/children) or the given tag. \\
	Optional count of articles to return and optional starting position (Paging)

## Acount management

* __POST / login__ -> attempt to log in to an existing account
```
	{
		username: string
		password: string
	}
```
* __POST / register__ -> attempt to register a new account
```
	{
		username: string
		password: string
		display_name: string
		email: string
	} 
```
	username needs to be unique
* __PUT / modify_user__ -> attempt to change account properties
```
	{
		username: string
		display_name: string
		email: string
		password: string
	} 
```
	all are optional, will remain unchanged if left empty; 
	if username is changed, the new username needs to be unique too.

