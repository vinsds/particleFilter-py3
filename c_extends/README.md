<h2>c_extends</h2>
<p>
La cartella contiene i moduli python per le funzioni:
<ul>
<li>normPdf</li>
<li>normRnd <i>(Box-Muller)</i></li>
</ul>
Queste, non essendo prensenti in ambiente, Python sono state implementate precedentemente in C ed in seguito sono state
 rese disponibili come singoli moduli Python.
</p>

<blockquote>

<b>Nota:</b> Per poter utilizzare queste funzioni, devono essere ricompilate per il proprio OS
<br >
<b style="display:block;">Mac OSX</b>
cd c_script
python3 setup_normpdf.py build
python3 setup_normpdf.py install
python3 setup_normrnd.py build
python3 setup_normrnd.py install<br />
Terminate queste operazioni, viene generata una cartella build all'interno di c_script. 
Prendere i file con estensione *.so e copiarli all'interno della cartella c_extends
</blockquote>
