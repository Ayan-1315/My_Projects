using UnityEngine;

public class SkyboxQualityManager : MonoBehaviour
{
    [Header("Skybox Materials")]
    public Material lowSkybox;
    public Material mediumSkybox;
    public Material highSkybox;
    public Material ultraSkybox;

    void Start()
    {
        ApplySkybox();
    }

    void ApplySkybox()
    {
        int quality = QualitySettings.GetQualityLevel();

        switch (quality)
        {
            case 0: // Low
                RenderSettings.skybox = lowSkybox;
                break;

            case 1: // Medium
                RenderSettings.skybox = mediumSkybox;
                break;

            case 2: // High
                RenderSettings.skybox = highSkybox;
                break;

            case 3: // Ultra
                RenderSettings.skybox = ultraSkybox;
                break;

            default:
                RenderSettings.skybox = mediumSkybox; // fallback
                break;
        }

        DynamicGI.UpdateEnvironment(); // refresh lighting
    }
}
