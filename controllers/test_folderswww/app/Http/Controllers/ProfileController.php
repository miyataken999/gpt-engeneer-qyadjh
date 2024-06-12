namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Profile;

class ProfileController extends Controller
{
    public function edit(User $user)
    {
        return view('profiles.edit', compact('user'));
    }

    public function update(User $user, Request $request)
    {
        $profile = $user->profile;
        $profile->bio = $request->input('bio');
        $profile->tags = $request->input('tags');
        $profile->save();

        return redirect()->route('users.show', $user);
    }
}