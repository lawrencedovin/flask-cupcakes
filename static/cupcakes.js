const BASE_URL = 'http://127.0.0.1:5000/api';

// $('.delete-todo').click(deleteTodo);

// async function deleteTodo() {
//     const id = $(this).data('id');
//     await axios.delete(`/api/todos/${id}`);
//     $(this).parent().remove();
// }

function generateCupcakeHTML(cupcake) {
    return `
    <div data-cupcake-id=${cupcake.id}>
        <li>
            ${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}
            <button class="delete-button">X</button>
        </li>
        <img class="cupcake-img"
             src="${cupcake.image}"
             alt="(no image provided)">
    </div>
    `;
}

async function showCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    for(let cupcakeData of response.data.cupcakes) {
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
    }
}

$("#create-cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();
  
    let flavor = $("#flavor-input").val();
    let rating = $("#rating-input").val();
    let size = $("#size-input").val();
    let image = $("#image-input").val();
  
    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
      flavor,
      rating,
      size,
      image
    });
  
    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#create-cupcake-form").trigger("reset");
});

$(showCupcakes);