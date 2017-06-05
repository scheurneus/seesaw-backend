# SPECS : 

* GET / -> index of the website
* GET / article / {id} -> webpage of the article {id}


* GET / articles -> webpage with a list of articles

* GET / articles / {oldest} | {newest} | {controversial} / ( {count} / ( {start} ) )
    -> list of articles sorted by oldest, newest, controversial... Optional count
    of articles to return and optional starting position (Paging)

* GET / articles / {parents} | {children} | {tagged} / {origin} / ( {count} / ( {start} ) )
    -> list of articles that are replied to by a given article, reply to a given article or have a given tag
	{origin} contains either the given article (in the case of parent/children) or the given tag
	Optional count of articles to return and optional starting position (Paging)



* POST / login -> attempt to log in to an existing account
	{
		username: string
		password: string
	}
* POST / register -> attempt to register a new account
	{
		username: string
		display_name: string
		email: string
	}
* PUT / modify_user -> attempt to change account properties
	{
		username: string
		display_name: string
		email: string
	} all are optional, will remain unchanged if left empty

* POST / articles -> Creates a new article
    {
        name: string
        text: string
        author: string
        formatting: string (plain / MD / HTML? / LaTeX?)        
		tag: array of strings
		replies_to: array of article ids
    }

* PUT / articles / {id} -> Updates the article {id}
    {
		title: string,
        content: string
    } both are optional, will remain unchanged if left out
* DELETE / articles / {id} -> Deletes the article {id} (requires a current session)
