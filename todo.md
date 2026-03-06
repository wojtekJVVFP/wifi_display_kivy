+do napisania kod do wyświetlania odebranej wiadomości w UI

+napisać odbiór wiadomości po stronie i wyświetlanie obrazka.Potrzebne są niektóre funkcje z 
poprzedniego projektu oraz funkcje do wyświetlania odebranego obrazka
- Uczyć się pisania interfejsu użytkownika w kivy
-- zarządzanie ułożeniem widgetów na ekranie

- Jak uruchomić serwer po wystartowaniu aplikacji tak, żeby najpierw pobrać od użytkownika adres IP do inicjalizacji serwera?
-- Może da się pobrać adres IP z urządzenia zamiast pobierać od użytkownika, natomiast w interfejsie wstępnym  pobrać informacji o urządzeniu
- Poprawiać kod do uzyskania uprawnień od użytkownika
- opóźnić start serwera, powinien się uruchomić po interfejsie, żeby była możliwość pobrania z telefonu adres IP

- rekonfiguracja serwera podczas działania - serwer może być wystartowany na początku jak zostanie pobrany ip
- może się zdarzyć, że serwer zostanie uruchomiony przed interfejsem i wtedy nie pobierze ip i wystartuje z nieprawidłowym ip
- zaimplementować screenmanager, drugie okno będzie służyć do wprowadzania ustawień programu i informacji o urządzeniu
+ uruchomić program na android
- testować na różnych wersjach android
- 



-automatyzacja procesu kompilowania i wgrywania oprogramowania do android
    +-jeden skrypt w linux, który skompiluje program i przeniesie program apk do windows
    --drugi skrypt wgra apk na telefon
--powinna być możliwość automatycznego kompilowania pod różne urządzenia

-debugowanie na emulatorze android studio, dodane kompilowanie także pod platformę X86/X64 do buildozer.spec.
Uruchamianie na emulatorze X64 będzie wtedy też możliwe, a taki emulator będzie szybszy

+uprawnienia działają na emulatorze, tylko aktualne nie wymagają potwierdzenia przez użytkownika