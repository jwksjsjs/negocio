#include "imgui.h"
#include "implot.h"
#include "backends/imgui_impl_glfw.h"
#include "backends/imgui_impl_opengl3.h"

#include <GLFW/glfw3.h>
#include <vector>
#include <string>
#include <cmath>
#include <random>
#include <chrono>
#include <thread>

// Classe base com configurações gráficas .
class Grafic {
protected:
    std::string xName = "Tempo";
    std::string yName = "Frequência";
    std::string graficTitle = "Gráfico de frequência";
    std::string graficColor = "g";
    std::string graficLabelLine = "Variação da frequência em função do tempo";

public:
    virtual void update() = 0;
    virtual void render() = 0;

    virtual ~Grafic() = default;
};


// Classe derivada que desenha e atualiza o gráfico
class GeneratedGrafic : public Grafic {
private:
    std::vector<float> x;
    std::vector<float> y;
    float timeElapsed = 0.0f;
    std::default_random_engine engine;
    std::uniform_int_distribution<int> dist;

public:
    GeneratedGrafic() : dist(1, 100) {
        x.push_back(0.0f);
        y.push_back(std::sin(0.0f));
    }

    void update() override {
        for (int i = 0; i < 10; ++i) {
            float val = std::sin(timeElapsed * dist(engine));
            x.push_back(timeElapsed);
            y.push_back(val);
            timeElapsed += 0.1f;
        }
    }

    void render() override {
        if (ImPlot::BeginPlot(graficTitle.c_str())) {
            ImPlot::SetupAxes(xName.c_str(), yName.c_str(), ImPlotAxisFlags_AutoFit, ImPlotAxisFlags_AutoFit);
            ImPlot::PlotLine(graficLabelLine.c_str(), x.data(), y.data(), x.size());
            ImPlot::EndPlot();
        }
    }
};


int main() {
    if (!glfwInit()) return -1;

    GLFWwindow* window = glfwCreateWindow(1280, 720, "Gráfico POO", NULL, NULL);
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    // Inicialização do ImGui
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImPlot::CreateContext();
    ImGuiIO& io = ImGui::GetIO();
    ImGui::StyleColorsDark();

    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init("#version 130");

    // Instância do gráfico
    GeneratedGrafic grafico;

    // Loop principal
    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();
        grafico.update();

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        ImGui::Begin("Painel");
        grafico.render();
        ImGui::End();

        ImGui::Render();
        int display_w, display_h;
        glfwGetFramebufferSize(window, &display_w, &display_h);
        glViewport(0, 0, display_w, display_h);
        glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

        glfwSwapBuffers(window);
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }

    // Finalização
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImPlot::DestroyContext();
    ImGui::DestroyContext();
    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}

