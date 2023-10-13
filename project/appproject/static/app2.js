
// Gallery
//
// Napisz prostą galerię. Po naciśnięciu miniatury zdjęcia powinno się ono pokazywać w trybie pełnego ekranu. Będzie się to działo przez dodanie nowego elementu w chwili, w której ktoś kliknie na daną miniaturę. Zadanie podzielone jest na punkty. Pamiętaj, żeby trzymać się dokładnie treści punktów i robić je po kolei.
// Punkt 1
//
// Zapoznaj się z kodem HTML i CSS dodanym do zadania. Do zrobienia galerii zazwyczaj używany odpowiednio wystylowanej listy, w której znajdują się obrazki. Lista zazwyczaj spełnia następujące zależności:
//
//     Nie ma żadnych stylów.
//     Ma szerokość i wysokość odpowiednią do wyświetlenia jednego obrazka.
//     Wszystkie obrazki mają tę samą szerokość i wysokość.
//     Wszystkie obrazki są widoczne.
//
// W kodzie HTML dodaj (ręcznie) w odpowiednie miejsce klasę gallery.
// Punkt 2
//
// Przygotuj do pracy plik app.js. Następnie znajdź następujące elementy i zapisz je do zmiennych:
//
//     Wszystkie elementy listy (zapisz do tablicy).
//     Tag body (będzie nam potrzebny do dodania elementu, który pokaże się na pełnym ekranie).
//
// Wypisz zmienne w konsoli, żeby upewnić się, czy zawierają poprawne dane.
// Punkt 3
//
// Do wszystkich obrazków dodaj event reagujący na kliknięcie. Najpierw może wypisywać "działa" w konsoli.
// Punkt 4
//
// Zmodyfikuj event w taki sposób, żeby w konsoli wypisywał adres URL klikniętego obrazka. Użyj do tego this.
// Punkt 5
//
// Zauważ, że na górze pliku app.js jest zakomentowany kawałek kodu HTML. Jest to wzór elementu, który ma zostać dodany do strony.
//     Przeanalizuj go, a następnie zmodyfikuj event dla obrazków w taki sposób, żeby tworzyć takie elementy i dodawały go do tagu body.
//     Pamiętaj o tym, żeby pod adres URL obrazka podłożyć odpowiednie dane.
// Punkt 6
//
// Po kliknięciu na obrazek powinien nam się wyświetlać powiększony obrazek + guzik. Musisz teraz dopisać event reagujący na kliknięcie w guzik.
//     Ma on spowodować usunięcie nowo stworzonego elementu z drzewa DOM.
// Punkt 7
//
// Sprawdź, jak działa Twoja strona. Czy widzisz problemy? Napisz.
//
//
// /*
//  <div class="fullScreen">
//    <img src="./images/wrong.png">
//    <button class="close">Close</button>
//  </div>
//  */
//

const listLi = document.querySelectorAll("ul li");
const tagBody = document.querySelector("body");

listLi.forEach(function (li) {
  li.addEventListener("click", function () {
    const imgSrc = this.querySelector("img").src;
    // const imgSrc = imgElement.getAttribute("src");

    // Tworzenie elementu div
    const newDiv = document.createElement("div");
    newDiv.classList.add("fullScreen");

            // Dodawanie div do body
    tagBody.appendChild(newDiv);


    // Tworzenie elementu img
    const img = document.createElement("img");
    img.setAttribute("src", imgSrc);

    // Tworzenie elementu button
    const closeButton = document.createElement("button");
    closeButton.classList.add("close");
    closeButton.innerText = "Close";

    // Dodawanie img i closeButton do div
    newDiv.appendChild(img);
    newDiv.appendChild(closeButton);





    // Event listener dla przycisku "Close"
    closeButton.addEventListener("click", function () {
      tagBody.removeChild(newDiv);
    });
  });
});

/*
<div class="fullScreen">
 <img src="./images/wrong.png">
 <button class="close">Close</button>
</div>
*/
//
// const galleryImages = document.querySelector("ul.gallery").querySelectorAll("li");
// const body = document.querySelector("body");
//
// const addFullScreenElements = (url) => {
//   const div = document.createElement("div");
//   div.classList.add("fullScreen");
//   const img = document.createElement("img");
//   img.src = url;
//   div.appendChild(img);
//   const button = document.createElement("button");
//   button.classList.add("close");
//   button.innerText = "Close";
//   div.appendChild(button);
//   body.appendChild(div);
// };
//
// const addFullScreenEventHandling = () => {
//   const div = document.querySelector("div.fullScreen");
//   const button = document.querySelector("button.close");
//   const handleClick = () => {
//     button.removeEventListener("click", handleClick);
//     div.parentElement.removeChild(div);
//   }
//   button.addEventListener("click", handleClick);
// }
//
// const handleClick = function(event) {
//  const url = this.querySelector("img").src;
//  addFullScreenElements(url);
//  addFullScreenEventHandling();
// }
//
// galleryImages.forEach((image) => {
//   image.addEventListener("click", handleClick);
// });