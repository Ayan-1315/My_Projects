from diffusers import StableDiffusionPipeline
import torch
import gradio as gr

# Load the model (make sure you have access)
model_id = "runwayml/stable-diffusion-v1-5"

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", 
    torch_dtype=torch.float16
).to("cuda")
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image(prompt, guidance_scale, steps, seed):
    generator = torch.manual_seed(seed) if seed else None
    image = pipe(prompt, guidance_scale=guidance_scale, num_inference_steps=steps, generator=generator, height=512, width=512).images[0]
    return image

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## Text to Image with Stable Diffusers")

    with gr.Row():
        prompt = gr.Textbox(label="Prompt", placeholder="Enter your image description here")
        seed = gr.Number(label="Seed (optional)", value=42, precision=0)
    
    with gr.Row():
        guidance = gr.Slider(minimum=1, maximum=20, value=7.5, step=0.5, label="Guidance Scale")
        steps = gr.Slider(minimum=10, maximum=100, value=50, step=1, label="Inference Steps")
    
    generate_button = gr.Button("Generate Image")
    output_image = gr.Image(label="Generated Image")

    generate_button.click(fn=generate_image, inputs=[prompt, guidance, steps, seed], outputs=output_image)

demo.launch()
