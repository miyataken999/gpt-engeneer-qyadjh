namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Team;

class TeamController extends Controller
{
    public function index()
    {
        $teams = Team::all();
        return view('teams.index', compact('teams'));
    }

    public function create(Request $request)
    {
        $team = new Team();
        $team->name = $request->input('name');
        $team->save();

        return redirect()->route('teams.index');
    }
}