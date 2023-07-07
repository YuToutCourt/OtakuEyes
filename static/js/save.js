function storeAnimeAndEpisode(episode, id, image, title) {
    
    if (episode == -1) return;
    
    var newEpisode = episode;
    var animeId = id;
    var animeImage = image;
    var animeTitle = title;

    // Retrieve stored anime data from local storage
    var storedAnime = localStorage.getItem('anime');
    console.log(storedAnime);

    if (storedAnime) {
        // Parse the stored anime data from JSON to an array of objects
        var storedAnimeArray = JSON.parse(storedAnime);

        // Check if the anime with the same ID already exists in local storage
        var existingAnime = storedAnimeArray.find(function(anime) {
            return anime.id === animeId;
        });

        if (existingAnime) {
            // Update the episode for the existing anime
            existingAnime.episode = newEpisode;
        } else {
            // Check the maximum number of stored anime entries (5)
            if (storedAnimeArray.length >= 5) {
                // Remove the oldest anime entry from the beginning of the array
                storedAnimeArray.shift();
            }

            // Add the new anime entry to the end of the array
            var newAnime = {
                episode: newEpisode,
                id: animeId,
                image: animeImage,
                title: animeTitle
            };
            storedAnimeArray.push(newAnime);
        }

        // Store the updated anime data back in local storage
        localStorage.setItem('anime', JSON.stringify(storedAnimeArray));
    } else {
        // No anime stored in local storage, create a new array with the current anime entry
        var animeArray = [{
            episode: newEpisode,
            id: animeId,
            image: animeImage,
            title: animeTitle
        }];
        localStorage.setItem('anime', JSON.stringify(animeArray));
    }
}
function loadLocalStorage() {
    var storedAnime = localStorage.getItem('anime');

    if (storedAnime) {
        // Parse the stored anime data from JSON to an array of objects
        var storedAnimeArray = JSON.parse(storedAnime);

        // Get the anime-list element
        var animeList = document.getElementById('anime-list');
        var h3 = document.createElement('h3');
        h3.appendChild(document.createTextNode('Continue watching'));
        document.getElementsByClassName('container')[0].insertBefore(h3, document.getElementById('anime-list'));

        // Loop through the stored anime data and create HTML elements for each entry
        storedAnimeArray.forEach(function(anime_) {
            
            // Create HTML elements for anime entry
            var article = document.createElement('article');

            var linkImage = document.createElement('a');
            linkImage.setAttribute('href', `anime/${anime_['id']}/${anime_['episode']}/vostfr`);

            var image = document.createElement('img');
            image.setAttribute('src', anime_['image']);
            image.setAttribute('class', 'coverimage');

            var linkTitle = document.createElement('a');
            linkTitle.setAttribute('href', `anime/${anime_['id']}/${anime_['episode']}/vostfr`);
            linkTitle.setAttribute('class', 'title');
            var titleText = document.createTextNode(`${anime_['title']} - Ep ${anime_['episode']}`);
            linkTitle.appendChild(titleText);

            // Append elements to the article
            linkImage.appendChild(image);
            article.appendChild(linkImage);
            article.appendChild(linkTitle);

            // Append the article to the anime-list element
            animeList.appendChild(article);
        });
    }
};