import logging
import qt
import slicer
import slicer.ScriptedLoadableModule
import slicer.util

# from Resources import HomeResourcesResources


class Home(slicer.ScriptedLoadableModule.ScriptedLoadableModule):
    """
    Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        slicer.ScriptedLoadableModule.ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = (
            "Home"  # TODO make this more human readable by adding spaces
        )
        self.parent.categories = [""]
        self.parent.dependencies = []
        self.parent.contributors = ["Sam Horvath (Kitware Inc.)"]
        self.parent.helpText = """This is the Home module for the custom application"""
        self.parent.helpText += self.getDefaultModuleDocumentationLink()
        self.parent.acknowledgementText = (
            """..."""  # replace with organization, grant and thanks.
        )


class HomeWidget(
    slicer.ScriptedLoadableModule.ScriptedLoadableModuleWidget,
    slicer.util.VTKObservationMixin,
):
    """
    Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        slicer.ScriptedLoadableModule.ScriptedLoadableModuleWidget.__init__(
            self, parent
        )
        slicer.util.VTKObservationMixin.__init__(self)

    def setup(self):
        slicer.ScriptedLoadableModule.ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer)
        self.uiWidget = slicer.util.loadUI(self.resourcePath("UI/Home.ui"))
        self.layout.addWidget(self.uiWidget)
        self.ui = slicer.util.childWidgetVariables(self.uiWidget)

        # Remove unneeded UI elements
        self.modifyWindowUI()

        # Create logic class
        self.logic = HomeLogic()

        # setup scene defaults
        self.setupNodes()

        # Dark palette does not propagate on its own?
        self.uiWidget.setPalette(slicer.util.mainWindow().style().standardPalette())

        # Apply style
        self.applyApplicationStyle()

        # Buttons
        self.ui.VPAWVisualizeButton.connect("clicked(bool)", self.onVPAWVisualizeButton)
        self.ui.VPAWModelButton.connect("clicked(bool)", self.onVPAWModelButton)

    def setupNodes(self):
        # Set up the layout / 3D View
        self.logic.setup3DView()
        self.logic.setupSliceViewers()

    def onClose(self, unusedOne, unusedTwo):
        pass

    def cleanup(self):
        pass

    def hideSlicerUI(self):
        slicer.util.setDataProbeVisible(False)
        slicer.util.setMenuBarsVisible(False, ignore=["MainToolBar", "ViewToolBar"])
        slicer.util.setModuleHelpSectionVisible(False)
        slicer.util.setModulePanelTitleVisible(False)
        slicer.util.setPythonConsoleVisible(False)
        slicer.util.setToolbarsVisible(True)
        slicer.util.findChild(slicer.util.mainWindow(), "MainToolBar")
        keepToolbars = [
            slicer.util.findChild(slicer.util.mainWindow(), "MainToolBar"),
            slicer.util.findChild(slicer.util.mainWindow(), "ViewToolBar"),
            slicer.util.findChild(slicer.util.mainWindow(), "CustomToolBar"),
        ]
        slicer.util.setToolbarsVisible(False, keepToolbars)

    def showSlicerUI(self):
        slicer.util.setDataProbeVisible(True)
        slicer.util.setMenuBarsVisible(True)
        slicer.util.setModuleHelpSectionVisible(True)
        slicer.util.setModulePanelTitleVisible(True)
        slicer.util.setPythonConsoleVisible(True)
        slicer.util.setToolbarsVisible(True)

    def modifyWindowUI(self):
        slicer.util.setModuleHelpSectionVisible(False)

        mainToolBar = slicer.util.findChild(slicer.util.mainWindow(), "MainToolBar")

        self.CustomToolBar = qt.QToolBar("CustomToolBar")
        self.CustomToolBar.name = "CustomToolBar"
        slicer.util.mainWindow().insertToolBar(mainToolBar, self.CustomToolBar)

        # centralaa = slicer.util.findChild(
        #     slicer.util.mainWindow(), name="CentralWidget"
        # )
        # central.setStyleSheet("background-color: #464449")

        gearIcon = qt.QIcon(self.resourcePath("Icons/Gears.png"))
        self.settingsAction = self.CustomToolBar.addAction(gearIcon, "")

        self.settingsDialog = slicer.util.loadUI(self.resourcePath("UI/Settings.ui"))
        self.settingsUI = slicer.util.childWidgetVariables(self.settingsDialog)

        self.settingsUI.CustomUICheckBox.toggled.connect(self.toggleUI)
        self.settingsUI.CustomStyleCheckBox.toggled.connect(self.toggleStyle)

        self.settingsAction.triggered.connect(self.raiseSettings)
        self.hideSlicerUI()

    def toggleStyle(self, visible):
        if visible:
            self.applyApplicationStyle()
        else:
            slicer.app.styleSheet = ""

    def toggleUI(self, visible):
        if visible:
            self.hideSlicerUI()
        else:
            self.showSlicerUI()

    def raiseSettings(self, unused):
        self.settingsDialog.exec()

    def applyApplicationStyle(self):
        # Style
        self.applyStyle([slicer.app], "Home.qss")

    def applyStyle(self, widgets, styleSheetName):
        stylesheetfile = self.resourcePath(styleSheetName)
        with open(stylesheetfile, "r") as fh:
            style = fh.read()
            for widget in widgets:
                widget.styleSheet = style

    def onVPAWVisualizeButton(self):
        """
        Switch to the "VPAW Visualize" module when the user clicks the button.
        """
        slicer.util.selectModule("VPAWVisualize")

    def onVPAWModelButton(self):
        """
        Switch to the "VPAW Model" module when the user clicks the button.
        """
        slicer.util.selectModule("VPAWModel")


class HomeLogic(slicer.ScriptedLoadableModule.ScriptedLoadableModuleLogic):
    """
    This class should implement all the actual computation done by your module.  The
    interface should be such that other python code can import this class and make use
    of the functionality without requiring an instance of the Widget.  Uses
    ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
        """
        Run the actual algorithm
        """

        pass

    def exitApplication(self, status=slicer.util.EXIT_SUCCESS, message=None):
        """
        Exit application.  If ``status`` is ``slicer.util.EXIT_SUCCESS``, ``message`` is
        logged using ``logging.info(message)`` otherwise it is logged using
        ``logging.error(message)``.
        """

        def _exitApplication():
            if message:
                if status == slicer.util.EXIT_SUCCESS:
                    logging.info(message)
                else:
                    logging.error(message)
            slicer.util.mainWindow().hide()
            slicer.util.exit(slicer.util.EXIT_FAILURE)

        qt.QTimer.singleShot(0, _exitApplication)

    # settings for 3D view
    def setup3DView(self):
        slicer.app.layoutManager()
        # layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
        # controller = slicer.app.layoutManager().threeDWidget(0).threeDController()
        # controller.setBlackBackground()
        # controller.set3DAxisVisible(False)
        # controller.set3DAxisLabelVisible(False)
        # controller.setOrientationMarkerType(3)  #Axis marker
        # controller.setStyleSheet("background-color: #000000")

    def setupSliceViewers(self):
        for name in slicer.app.layoutManager().sliceViewNames():
            sliceWidget = slicer.app.layoutManager().sliceWidget(name)
            self.setupSliceViewer(sliceWidget)

        # Set linked slice views in all existing slice composite nodes and in the
        # default node
        sliceCompositeNodes = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
        defaultSliceCompositeNode = slicer.mrmlScene.GetDefaultNodeByClass(
            "vtkMRMLSliceCompositeNode"
        )
        if not defaultSliceCompositeNode:
            defaultSliceCompositeNode = slicer.mrmlScene.CreateNodeByClass(
                "vtkMRMLSliceCompositeNode"
            )
            # CreateNodeByClass is factory method, need to unregister the result to
            # prevent memory leaks:
            defaultSliceCompositeNode.UnRegister(None)
            slicer.mrmlScene.AddDefaultNode(defaultSliceCompositeNode)
        sliceCompositeNodes.append(defaultSliceCompositeNode)
        for sliceCompositeNode in sliceCompositeNodes:
            sliceCompositeNode.SetLinkedControl(True)

    # Settings for slice views
    def setupSliceViewer(self, sliceWidget):
        sliceWidget.sliceController()
        # controller.setOrientationMarkerType(3)  #Axis marker
        # controller.setRulerType(1)  #Thin ruler
        # controller.setRulerColor(0) #White ruler
        # controller.setStyleSheet("background-color: #000000")
        # controller.sliceViewLabel = ''


class HomeTest(slicer.ScriptedLoadableModule.ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """
        Do whatever is needed to reset the state - typically a scene clear will be
        enough.
        """
        slicer.mrmlScene.Clear(0)

    def runTest(self):
        """Run as few or as many tests as needed here."""
        self.setUp()
        self.test_Home1()

    def test_Home1(self):
        """
        Ideally you should have several levels of tests.  At the lowest level tests
        should exercise the functionality of the logic with different inputs (both valid
        and invalid).  At higher levels your tests should emulate the way the user would
        interact with your code and confirm that it still works the way you intended.

        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on, your
        test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")
        #
        # first, get some data
        #

        HomeLogic()
        self.delayDisplay("Test passed!")


#
# Class for avoiding python error that is caused by the method SegmentEditor::setup
# http://issues.slicer.org/view.php?id=3871
#
class HomeFileWriter(object):
    def __init__(self, parent):
        pass
