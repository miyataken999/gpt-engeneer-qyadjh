Route::get('/', function () {
    return view('welcome');
});

Route::post('/register', 'UserController@register');
Route::post('/login', 'UserController@login');
Route::get('/users', 'UserController@index');
Route::get('/users/{user}', 'UserController@show');

Route::get('/teams', 'TeamController@index');
Route::post('/teams', 'TeamController@create');

Route::get('/profiles/{user}/edit', 'ProfileController@edit');
Route::patch('/profiles/{user}', 'ProfileController@update');