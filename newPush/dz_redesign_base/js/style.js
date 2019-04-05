function switchSignUp() {
	document.getElementById('card__signIn').className = 'hidden';
	document.getElementById('card__signUp').className = 'show';
	document.getElementById('mobile__auth').className = 'hidden';
}

function switchSignIn() {
	document.getElementById('card__signUp').className = 'hidden';
	document.getElementById('card__signIn').className = 'show';
	document.getElementById('mobile__auth').className = 'hidden';
}
