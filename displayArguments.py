from xml.etree import ElementTree
from xml.dom import minidom
from xml.sax.saxutils import escape
import forum
import post

def prettify(elem):
    #Return a pretty-printed XML string for the Element
    roughString = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(roughString)
    return reparsed

def constructSinglePostXML(top, forumPost):

    post = ElementTree.SubElement(top, 'post')

    website = ElementTree.SubElement(post, 'website')
    website.text = escape(forumPost.getUrl())

    originalMessage = ElementTree.SubElement(post, 'originalMessage')
    originalMessage.text = escape(forumPost.getReview())

    rating = ElementTree.SubElement(post, 'rating')
    rating.text = forumPost.getRating()

    return post



def constructXML(forums):
    
    fileHandler = open("argumentsList.xml", "w")
    top = ElementTree.Element('allPosts')

    for forum in forums:
        forumPosts = forum.getPosts()

        
        for forumPost in forumPosts:
            singlePost = constructSinglePostXML(top, forumPost)

    prettifiedTop = prettify(top)

    prettifiedTop.writexml(fileHandler);

    fileHandler.close()

