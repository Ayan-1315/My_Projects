using UnityEngine;
using UnityEngine.SceneManagement;

public class MenuController : MonoBehaviour
{
    // Load Game Scene
    public void PlayGame()
    {
        SceneManager.LoadScene(2, LoadSceneMode.Single);
    }

    // Load Settings Scene
    public void OpenSettings()
    {
        MusicManager.Instance?.ResetToPreTap(); // also play pre-tap in Settings
        SceneManager.LoadScene(1, LoadSceneMode.Single);
    }

    // Go back to Main Menu
    public void BackToMainMenu()
    {
        MusicManager.Instance?.ResetToPreTap(); // ensure pre-tap plays on MainMenu
        SceneManager.LoadScene(0, LoadSceneMode.Single);
    }

    // Quit the game
    public void QuitGame()
    {
        Application.Quit();
        Debug.Log("Game Quit!"); // works only in build, not editor
    }
}
