const students = [
    'student-1', 'student-2', 'student-3', 'student-4', 'student-5',
	'student-6', 'student-7', 'student-8', 'student-9'
]

const columnTemplate = document.getElementsByClassName('column-template')[0];
for (let i=0; i < students.length; i++) {
	let studentName = students[i].toLocaleLowerCase().split(' ').join('-')

	// Set ID an Class.
	var newCol = columnTemplate.cloneNode(true);
	newCol.setAttribute('id', `std-${i+1}`);
	newCol.setAttribute('class', 'column');

	// Set the picture.
	let picture = newCol.getElementsByClassName("picture")[0];
	picture.setAttribute('src', `pictures/${studentName}.png`)

	// Set the name.
	let nameElement = newCol.getElementsByClassName("student-name")[0];
	nameElement.innerHTML = students[i];

	// The end!
	newCol.setAttribute('style', 'height: 30%');
	container.appendChild(newCol);
}

