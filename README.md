# Future Enginners - MacRobot

![MacRobot](https://user-images.githubusercontent.com/98695515/175649754-faef9d9c-d74e-4d6a-8ee8-871db03e8625.JPG)

Dieses Repository enthält alle wichtigen Dateien zu unserem autonom fahrenden Auto “MacRobot” (stammt von der Fernsehserie MacGyver). Als Basis/Mikrocontroller haben wir uns für den Lego Mindstorms EV3 entschieden, welchen wir mit der PixyCam CMUcam5 V1 (Lego Mindstorms Version) für die Objekterkennung ausgestattet haben. Der Grund für die Wahl des EV3 waren die hohe Zuverlässigkeit sowie die bereits vorhandenen Kenntnisse und Erfahrung mit dem System inkl. Programmierung. Das Programm für den regionalen Wettbewerb haben wir in der Lego eigenen Software entwickelt und lief auf einem EV3-Brick mit der originalen Lego Mindstorms EV3 Firmware. Für das Deutschlandfinale sind wir einen Schritt weiter gegangen und haben den EV3-Brick auf Basis der ev3dev-Firmware mit Python programmiert.

Programmstruktur:
Da wir für die beiden Rennmodi verschiedene Sensoren verwenden, erstellten wir ein Script für das Rennen ohne Hindernisse (siehe “/Programmcode/Python/Non-Obstacles”) sowie ein Script für das Hindernisrennen (siehe “/Programmcode/Python/Obstacles”). Außerdem schrieben wir ein Modul (siehe "/Programmcode/Python/libraryFE"), welches wichtige Funktionen für “Obstacles” und “Non-Obstacles” beinhaltet. Beispiel dafür ist die myPID-Klasse, welche einen PID-Regler zur Verfügung stellt und Motorwerte aus Soll-Werten und Ist-Werten berechnet.

Motoren/Sensoren:
Der MacRobot wird von einem Lego EV3 Medium-Motor über die Hinterachse mit Differential (bessere Kurvenfahrt) angetrieben. Für die Lenkung haben wir ebenfalls einen Lego EV3 Medium-Motor verwendet. Um den Bot möglichst genau geradeaus fahren zu lassen, verbauten wir einen Lego-Gyrosensor, welcher nach dem Start zurückgesetzt wird und dann die Drehposition misst. Des Weiteren erkennt ein Lego-Farbsensor, ob eine farbige Linie überfahren wird. Dies ist nützlich, um einerseits die Abschnitte zu zählen und nach drei Runden stehen zu bleiben und andererseits eine Kurve einzuleiten. Vor einem Hindernisrennen montieren wir die bereits erwähnte PixyCam, um die roten und grünen Hindernisse zu umfahren. Es ist uns nicht gelungen, mit der Kamera die dicken und farbigen Linien von den Hindernissen zu unterscheiden und diese sinnvoll auszuwerten, um auf einen Farbsensor zu verzichten. Während einem Rennen ohne Hindernisse orientiert sich der Roboter außerdem mithilfe von zwei Lego-Ultraschallsensoren, welche die Abstände zu den Wänden messen.

Software:
Programmiert haben wir die .ev3 in der Lego eigenen LabView-Umgebung und die .py in Microsoft Visual Studio Code mit der ev3dev-Extension. Das 3D-Modell, die technische Zeichnung und die Darstellung der elektrischen Komponenten wurden in Autodesk Fusion 360 erstellt. Das Design für unsere T-Shirts haben wir in Photoshop erstellt und später in unserem Heimatort bedrucken lassen.

Über uns:
Wir kommen aus Chemnitz und heißen Lenny Stelzmann und Fabian Zänker. Schon seit wir uns in der 5. Klasse kennengelernt haben, konnten wir uns für Technik und Informatik begeistern. Aktuell sind wir Schüler der 12. Klasse und arbeiten (hart) an unserem Abitur.
Wir danken recht herzlich unserem Sponsor “maker e.V”, welcher uns das Bedrucken von eigenen Teamshirts ermöglichte.
