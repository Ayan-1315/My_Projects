using UnityEngine;

public class SettingsBootstrapper : MonoBehaviour
{
    private static SettingsBootstrapper _instance;

    [Header("Skybox Materials by Quality")]
    public Material lowSkybox;
    public Material mediumSkybox;
    public Material highSkybox;
    public Material ultraSkybox;

    private void Awake()
    {
        // singleton so it survives once
        if (_instance != null && _instance != this)
        {
            Destroy(gameObject);
            return;
        }
        _instance = this;
        DontDestroyOnLoad(gameObject);

        ApplySaved(); // apply on boot
    }

    public static void ApplySaved()
    {
        int quality = PlayerPrefs.GetInt("QualityLevel", 1); // 0=Low,1=Medium,2=High,3=Ultra
        int fps = PlayerPrefs.GetInt("TargetFPS", 60);       // 30/60/90/120

        // Apply Quality
        QualitySettings.SetQualityLevel(Mathf.Clamp(quality, 0, 3), true);
        QualitySettings.vSyncCount = 0;               // let targetFrameRate control FPS
        Application.targetFrameRate = Mathf.Clamp(fps, 30, 120);

        // Apply Skybox
        if (_instance != null)
            _instance.ApplySkybox(quality);
    }

    private void ApplySkybox(int quality)
    {
        switch (quality)
        {
            case 0: RenderSettings.skybox = lowSkybox; break;
            case 1: RenderSettings.skybox = mediumSkybox; break;
            case 2: RenderSettings.skybox = highSkybox; break;
            case 3: RenderSettings.skybox = ultraSkybox; break;
        }

        // refresh lighting
        DynamicGI.UpdateEnvironment();
    }
}
