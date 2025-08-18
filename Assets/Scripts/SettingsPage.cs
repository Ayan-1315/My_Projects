using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class SettingsPage : MonoBehaviour
{
    [Header("UI (Legacy)")]
    public Dropdown qualityDropdown; // 0=Low,1=Medium,2=High,3=Ultra
    public Dropdown fpsDropdown;     // 0=30,1=60,2=90,3=120

    private readonly int[] fpsValues = { 30, 60, 90, 120 };

    private void Start()
    {
        // safety checks
        if (qualityDropdown == null || fpsDropdown == null)
        {
            Debug.LogError("Assign QualityDropdown and FpsDropdown in the inspector.");
            return;
        }

        // load saved
        int savedQuality = PlayerPrefs.GetInt("QualityLevel", 2);
        int savedFps = PlayerPrefs.GetInt("TargetFPS", 60);

        qualityDropdown.value = Mathf.Clamp(savedQuality, 0, 3);
        qualityDropdown.RefreshShownValue();

        int fpsIndex = 1; // default 60
        for (int i = 0; i < fpsValues.Length; i++)
        {
            if (fpsValues[i] == savedFps) { fpsIndex = i; break; }
        }
        fpsDropdown.value = fpsIndex;
        fpsDropdown.RefreshShownValue();
    }

    // Save button
    public void Save()
    {
        int qIndex = Mathf.Clamp(qualityDropdown.value, 0, 3);
        int fps = fpsValues[Mathf.Clamp(fpsDropdown.value, 0, fpsValues.Length - 1)];

        // apply now
        QualitySettings.SetQualityLevel(qIndex, true);
        QualitySettings.vSyncCount = 0;
        Application.targetFrameRate = fps;

        // persist
        PlayerPrefs.SetInt("QualityLevel", qIndex);
        PlayerPrefs.SetInt("TargetFPS", fps);
        PlayerPrefs.Save();

        // also update bootstrapper if already alive
        SettingsBootstrapper.ApplySaved();

        Debug.Log($"Saved Settings -> Quality: {qIndex}, FPS: {fps}");
    }

    // Back button
    public void BackToMainMenu()
    {
        SceneManager.LoadScene("MainMenu");
    }

    private void Update()
    {
        // Android back button
        if (Input.GetKeyDown(KeyCode.Escape))
            BackToMainMenu();
    }
}
