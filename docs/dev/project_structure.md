# Project Structure

## kb
Place for the knowledge base of your app. Put your *.scs* files here.

## problem-solver
Place for the problem solver of your app. Put your agents here.

### Agents on C++
Some tips:

- Store your modules with c++ agents in *problem-solver/cxx*;

- After update c++ code you need to rebuild problem-solver. Just run:
```
cd idesa/scripts
./build_problem_solver.sh
```
For a full rebuild with the deleting of the *bin* and *build* folders run:
```
cd idesa/scripts
./build_problem_solver.sh -f
```
For build tests run:
```
cd idesa/scripts
./build_problem_solver.sh -t
```
For a full rebuild with build tests and the deleting of the *bin* and *build* folders run:
```
cd idesa/scripts
./build_problem_solver.sh -f -t
```

- Add an action deactivation check by using a function *ActionUtils::isActionDeactivated()* from the common module. Identifiers of actions for deactivating are stored in *kb/non_subject_domain_concepts/action_deactivated.scs*. Example:
```
#include "utils/ActionUtils.hpp"

sc_result MyModule::InitializeImpl()
{
  ScMemoryContext ctx(sc_access_lvl_make_min, "MyModule");
  if (ActionUtils::isActionDeactivated(&m_memoryCtx, Keynodes::action_of_my_agent))
  {
    SC_LOG_ERROR("My agent action is deactivated")
  }
  else
  {
    ...
  }
  return SC_RESULT_OK;
}
```

- For enable debug:

    * add *SET(CMAKE_BUILD_TYPE Debug)* line 
    to *idesa/CMakeLists.txt* file;
    * rebuild problem-solver.

### Agents on Python
Some tips:

- Store your modules with python agents in *problem-solver/py*;
- After updating the python code you don't need to rebuild a problem-solver;
- Add an action deactivation check by using a function *is_action_deactivated()* from the common module. Identifiers of actions for deactivating are stored in *kb/non_subject_domain_concepts/action_deactivated.scs*. Example:
```
from common_module.searcher.common_constructions_searcher import is_action_deactivated
...
if is_action_deactivated(memory_ctx, action_of_my_agent):
    self.log.info('My agent action is deactivated')
else:
    ...
```

- Check execution time of agent by using a decorator *@timing*. Example:
```
from common_module.test_module.utils.perf_utils import timing
...

@timing
def RunImpl(self, evt: ScEventParams) -> ScResult:
...
```

- [Profile](https://docs.python.org/3/library/profile.html) your agent by using a decorator *@profileit(agent_name)*. Statistics will be saved in *common_module/test_module/utils/stat/agent_name.stat*. Example:
```
from common_module.test_module.utils.perf_utils import profileit
...

@profileit("my_agent_name")
def RunImpl(self, evt: ScEventParams) -> ScResult:
...

```

### Logging
You can change the logging level by changing the value of a variable LOG_MODE. This variable is located in */aide/ostis-web-platform/sc-machine/CMakeLists.txt*

Note that after making changes to CMakeLists, a rebuild is required.

## interface
Place for your interface modules.

## scripts
Place for scripts of your app.

### build_problem_solver.sh [-f, --full]
Build the problem-solver of your app. Use an argument *-f* or *--full* for a complete rebuild of the problem-solver with the deleting of the *ostis-web-platform/sc-machine/bin* and *ostis-web-platform/sc-machine/build* folders.

### build_interface.sh
Build the interface of your app.

### install_project.sh
Install or update the OSTIS platform.

### install_subsystems.sh
Building a problem solver and a knowledge base of subsystems.
