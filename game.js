let randomProperty = function (obj) {
    let keys = Object.keys(obj);
    return keys[keys.length * Math.random() << 0];
};

let populateData = function (data) {
    let possibles = data.clues
    let hint = randomProperty(data.clues);
    let [answer, color, obj_type] = data.clues[hint];
    document.getElementById("hint").innerHTML = hint;
    document.getElementById("color").innerHTML = data.colors[color];
    document.getElementById("obj_type").innerHTML = data.types[obj_type];
    document.getElementById("answer").innerHTML = answer;
};

fetch('./cards.json')
  .then(response => response.json())
  .then(data => populateData(data));

