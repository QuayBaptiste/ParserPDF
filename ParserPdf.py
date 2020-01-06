import shutil   #pour suprimmer récursivement
import subprocess as sp #commande 
import os       #commande de base
import os.path  #le path du program
import sys      #argument 

# compare 2 strings without taking care of the capitals letters
def compareStr(str1, str2):
    if len(str1) == len(str2):
        cpt = 0
        while cpt < len(str1):
            if ord(str1[cpt]) == ord(str2[cpt]) or ord(str1[cpt]) == (ord(str2[cpt])+32) or ord(str1[cpt]) == (ord(str2[cpt])-32):
                cpt+=1
            else : return False
        return True
    return False


def isIn(str1, str2):
    if len(str1) == len(str2):
        return compareStr(str1,str2)
    elif len(str1) < len(str2):
        if not(compareStr(str1,str2[-len(str1):])):
            return compareStr(str1,str2[:len(str1)])
        else : 
            return compareStr(str1,str2[-len(str1):])
        

# Transform an element to a terminal friendly element
def transform(element):
    cpt = 0
    for i in element :
        if i == " " :
            element = element[:cpt] + '\ ' + element[cpt+1:]
            cpt+=1
        cpt+=1
    return element

def Abstract(Contenu):
    if "Abstract" in Contenu :
        begin = Contenu.split("Abstract",1)
    
    if "ABSTRACT" in Contenu :                                       
        begin = Contenu.split("ABSTRACT",1)                     
                       
    end="1 "
    
    if "Index" in Contenu :
        end = "Index"
    elif "Keywords" in Contenu :                                      
        end = "Keywords"
            
    
    try:
        begin
    except NameError:
        return "erreur"
    else:
        a = begin[1].split(end)
        b = a[0].split("\n")
        abstract = ''.join(b)
        return abstract

        

def findTitle(source, element):
    titleToPrint = title = author = tmpAuthor = ""
    debut = finished = False
    element = element[:-4]
    for char in element :
        if char == '_' or char == '-':
            break
        author+=char
    for ligne in source:
        if not debut :
            save = ""
            cpt = 0
            done = False
            while not done :
                for char in ligne :
                    if char == " " :
                        cpt+=1
                    if char == ":":
                        cpt+=1
                    if cpt < 2 and char != ":" :
                        save +=char
                if title == "" :
                    cpt = 0
                    for char in element :
                        if char == " " :
                            cpt+=1
                        if cpt < 2 and char != ":" :
                            title +=char
                            if char == "_" :
                                title = ""
                done = True
            if compareStr(title, save) : 
                debut = True
                titleToPrint = ligne
        elif (not finished):
            done = False
            for char in ligne :
                if (ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) :
                    tmpAuthor += char
                else :
                    if compareStr(author, tmpAuthor) : 
                        finished = True
                    else :
                        tmpAuthor = ""
            if not finished :
                titleToPrint = titleToPrint[:-1]
                titleToPrint = titleToPrint + " " +ligne
    return titleToPrint[:-1]

def findParts(source):
    introduction = corps = conclusion = discussion = bibliographie = False
    contenuIntro = "Introduction : "
    contenuCorps = "Corps : "
    contenuConclusion = "Conclusion : "
    contenuDiscussion = "Discussion : "
    contenuBibliographie = "Bibliographie : "
    for ligne in source:
        save = ""
        for char in ligne :
            if char != "\n":
                save += char
        if save != "":
            test = save.split(" ")
            test.extend(["none", "none", "none"])
            if not introduction :
                if compareStr(test[1], "introduction") :
                    introduction = True
            elif not(corps) :
                if (test[0] == '2' or test[0] == '2.' or test[0] == '2)' or test[0] == 'II' or test[0] == 'II.' or test[0] == 'II)'):
                    if test[1] != "none":
                        if not (test[1].startswith("http") or test[1] == "C.E."):
                            corps = True
                            contenuCorps += save + "  "
                else :
                    contenuIntro += save + "  "

            elif not (discussion or conclusion) :
                if (compareStr(test[1], "conclusion") or compareStr(test[1], "conclusions") ) :
                    conclusion = True
                elif (compareStr(test[1], "discussion") or compareStr(test[1], "discussions") ) :
                    discussion = True
                else :
                    contenuCorps += save + "  "
            elif not bibliographie :
                if (compareStr(test[1], "references") or compareStr(test[0], "references")) :
                    bibliographie = True
                elif (conclusion) :
                    if not (discussion) :
                        if (compareStr(test[1], "discussion") or compareStr(test[1], "discussions")) :
                            discussion = True
                        else : 
                            contenuConclusion += save + "  "
                if (discussion and not(bibliographie)) :
                    if not (conclusion) :
                        if (compareStr(test[1], "conclusion") or compareStr(test[1], "conclusions")) :
                            conclusion = True
                        else : 
                            contenuDiscussion += save + "  "
                    else:
                        contenuConclusion += save + "  "
            else :
                contenuBibliographie += save
    return [contenuIntro, contenuCorps, contenuConclusion, contenuDiscussion, contenuBibliographie]

def findauteur(source, element):
    debTitre = fin = False
    result=""
    titre = findTitle(source, element)
    source.close()
    source = open(element,"r")
    for ligne in source:
        ligne = ligne[:-1]
        if isIn(ligne, titre) and not debTitre :
            debTitre = True
        if not isIn(ligne, titre) and debTitre :
            if isIn("Abstract", ligne):
                print(ligne)
                fin = True
            if fin : 
                return result
            result += ligne + "  "
        


def resultat(xml, tmp, result, element):
    os.chdir(tmp)
    source = open(element,"r")
    destination = open(result+'/'+element, "w")

    print("Titre : " + findTitle(source, element), file = destination)
    source.close()

    nom = element[:-4] + '.pdf'
    print("\nnom du fichier : " + nom, file =destination)

    #if xml :
        #print(findauteur(source, element), file = destination)

    source = open(element,"r")
    txt = source.read()
    r = Abstract(txt)
    destination.write("\nResumé : ")
    for i in range(0,len(r)) :                                 
        destination.write(r[i])
    source.close()


    if xml :
        source = open(element,"r")
        liste = findParts(source)
        print("\n", file = destination)
        for i in liste :
            print(i, file = destination)
            print("", file = destination)
        source = open(element,"r")
        aut = findauteur(source, element)
        if (aut != None):
            print("auteur : " + aut, file = destination)
        source.close()

    destination.close()


def xml(directory,liste):
    aut = "Auteur introuvable"
    for element in os.listdir(directory):
        if element.endswith('.pdf'):
            if element in liste:
                if not os.path.exists(directory+"/xmlResultat"):
                    os.mkdir(directory+"/xmlResultat")
                element = element.replace(".pdf", "")
                source = open(directory+"/resultToXml/"+element+".txt", "r")              
                f = open(directory+"/xmlResultat/"+element+".xml", "w")
                i=1
                for line in source:
                    if i == 1:
                        t = line
                        t = t[8:-1]
                    if i == 3:
                        p = line
                        p = p[17:-1]
                    if i == 5:
                        a = line
                        a = a[9:-1]
                    if i == 7:
                        intr = line
                        intr = intr[15:-1]
                    if i == 9:
                        c = line
                        c = c[8:-1]
                    if i == 11:
                        ccl = line
                        ccl = ccl[13:-1]
                    if i == 13:
                        d = line
                        d = d[13:-1]
                    if i == 15:
                        b = line
                        b = b[16:-1]
                    if i == 17:
                        aut = line
                        aut = aut[9:-1]
                    i+=1

                f.write("<article>\n")          
                f.write("\t<preamble>"+p+"</preamble>\n")
                t = t.replace('&','&amp;')
                t = t.replace('<','&lt;') 
                t = t.replace('>','&gt;')
                t = t.replace("", " ")
                f.write("\t<titre>"+t+"</titre>\n")
                aut = aut.replace('&','&amp;')
                aut = aut.replace('<','&lt;') 
                aut = aut.replace('>','&gt;')
                aut = aut.replace("", " ")
                f.write("\t<auteur>"+aut+"</auteur>\n")
                a = a.replace('&','&amp;')
                a = a.replace('<','&lt;') 
                a = a.replace('>','&gt;')
                a = a.replace("", " ")
                f.write("\t<abstract>"+a+"</abstract>\n")
                intr = intr.replace('&','&amp;')
                intr = intr.replace('<','&lt;') 
                intr = intr.replace('>','&gt;')
                intr = intr.replace("", " ")
                f.write("\t<introduction>"+intr+"</introduction>\n")
                c = c.replace('&','&amp;')
                c = c.replace('<','&lt;') 
                c = c.replace('>','&gt;')
                c = c.replace("", " ")
                f.write("\t<corps>"+c+"</corps>\n")
                ccl = ccl.replace('&','&amp;')
                ccl = ccl.replace('<','&lt;') 
                ccl = ccl.replace('>','&gt;')
                ccl = ccl.replace("", " ")
                f.write("\t<conclusion>"+ccl+"</conclusion>\n")
                d = d.replace('&','&amp;')
                d = d.replace('<','&lt;') 
                d = d.replace('>','&gt;')
                d = d.replace("", " ")
                f.write("\t<discussion>"+d+"</discussion>\n")
                b = b.replace('&','&amp;')
                b = b.replace('<','&lt;') 
                b = b.replace('>','&gt;')
                b = b.replace("", " ")
                f.write("\t<biblio>"+b+"</biblio>\n")
                f.write("</article>")
                f.close()
                source.close()

def transmog(argv, directory):
    origin = "{0}/{1}".format(os.getcwd(), directory)
    xml = False
    if (argv[1] == "-t"):
        result = "{0}/{1}result".format(os.getcwd(), directory)
    else :
        result = "{0}/{1}resultToXml".format(os.getcwd(), directory)
        xml = True

    if os.path.exists(result):
        shutil.rmtree(result)
    os.mkdir(result)
    tmp = "{0}/{1}/tmp".format(os.getcwd(), directory)
    for element in os.listdir(tmp):
        if element.endswith('.txt'):
            resultat(xml, tmp, result, element)
    os.chdir(origin)
 
def pdf(directory,liste):
    tmp = "{}/tmp".format(directory)
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.mkdir(tmp)
    for element in os.listdir(directory):
        if element.endswith('.pdf'):
            if element in liste:
                element = transform(element)
                titre = element[0:-4]
                a = "pdftotext -raw -nopgbrk -enc ASCII7 {0}/{1}/{2}  {0}/{1}/tmp/{3}.txt".format(os.getcwd(),directory, element, titre)
                os.system(a)

def main(argv):               
    if len(argv) != 3:
        print("Deux arguments attendus !")
        print("-option attendu :")
        print(" -t  version .txt")
        print(" -x  version .xml")
        sys.exit(2)
    else:
        current = os.getcwd()
        if not (argv[2].endswith("/")) : directory = argv[2] +"/"
        else : directory = argv[2]
        if os.path.exists(directory) & os.path.isdir(directory):
            liste=[]
            for element in os.listdir(argv[2]):
                if element.endswith('.pdf'):
                    print("Voulez vous parser "+element+" ? (o/n)");
                    choix = input("Entrez votre choix:");
                    if choix == "o":
                        liste.append(element);
            pdf(directory,liste)
        else:
                print( "L'argument n'éxiste pas ou n'est pas un répertoire !")
                sys.exit(2)
        if argv[1] == "-t":
            transmog(argv, directory)
        elif argv[1] == "-x":
            transmog(argv, directory)
            os.chdir(current)
            xml(directory,liste)
            os.chdir(current+"/"+directory)
            os.system("rm -r resultToXml")
        else :
            print("-option non reconnue :")
            print(" -t  version .txt")
            print(" -x  version .xml")
        os.system("rm -r tmp")

                
main(sys.argv)
